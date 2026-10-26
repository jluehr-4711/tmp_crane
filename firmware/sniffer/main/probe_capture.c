// DOUT capture with the MCPWM capture unit: hardware timestamps (80 MHz) on both
// edges, so PWM up to several hundred kHz is measured without ISR jitter.
#include "sniffer.h"
#include "driver/mcpwm_cap.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "esp_log.h"

static const char *TAG = "cap";
static mcpwm_cap_timer_handle_t s_timer;
static mcpwm_cap_channel_handle_t s_chan;
static uint32_t s_res_hz = 80000000;
static portMUX_TYPE s_mux = portMUX_INITIALIZER_UNLOCKED;

// window accumulators, touched in ISR
static volatile uint32_t w_edges, w_periods;
static volatile uint64_t w_period_sum, w_high_sum;
static volatile uint32_t w_period_min = UINT32_MAX, w_period_max, w_high_min = UINT32_MAX, w_high_max;
static uint32_t s_last_rise, s_last_fall;
static bool s_have_rise, s_have_fall;

static bool IRAM_ATTR on_edge(mcpwm_cap_channel_handle_t ch, const mcpwm_capture_event_data_t *e, void *arg)
{
    uint32_t t = e->cap_value;
    w_edges++;
    if (e->cap_edge == MCPWM_CAP_EDGE_POS) {
        if (s_have_rise && s_have_fall) {
            uint32_t period = t - s_last_rise;          // unsigned wrap-safe
            uint32_t high   = s_last_fall - s_last_rise;
            if (high < period) {
                w_periods++;
                w_period_sum += period; w_high_sum += high;
                if (period < w_period_min) w_period_min = period;
                if (period > w_period_max) w_period_max = period;
                if (high < w_high_min) w_high_min = high;
                if (high > w_high_max) w_high_max = high;
            }
        }
        s_last_rise = t; s_have_rise = true;
    } else {
        s_last_fall = t; s_have_fall = true;
    }
    return false;
}

void probe_capture_init(void)
{
    mcpwm_capture_timer_config_t tcfg = {
        .clk_src = MCPWM_CAPTURE_CLK_SRC_DEFAULT,
        .group_id = 0,
    };
    ESP_ERROR_CHECK(mcpwm_new_capture_timer(&tcfg, &s_timer));
    mcpwm_capture_channel_config_t ccfg = {
        .gpio_num = PIN_CAPTURE,
        .prescale = 1,
        .flags.neg_edge = true,
        .flags.pos_edge = true,
        .flags.pull_up = false,
        .flags.pull_down = false,
    };
    ESP_ERROR_CHECK(mcpwm_new_capture_channel(s_timer, &ccfg, &s_chan));
    mcpwm_capture_event_callbacks_t cbs = { .on_cap = on_edge };
    ESP_ERROR_CHECK(mcpwm_capture_channel_register_event_callbacks(s_chan, &cbs, NULL));
    ESP_ERROR_CHECK(mcpwm_capture_channel_enable(s_chan));
    ESP_ERROR_CHECK(mcpwm_capture_timer_enable(s_timer));
    ESP_ERROR_CHECK(mcpwm_capture_timer_start(s_timer));
    ESP_ERROR_CHECK(mcpwm_capture_timer_get_resolution(s_timer, &s_res_hz));
    ESP_LOGI(TAG, "capture on GPIO%d, %lu Hz timestamps", PIN_CAPTURE, (unsigned long)s_res_hz);
}

void probe_capture_snapshot(capture_stats_t *o)
{
    uint32_t edges, periods, pmin, pmax, hmin, hmax; uint64_t psum, hsum;
    portENTER_CRITICAL(&s_mux);
    edges = w_edges; periods = w_periods; psum = w_period_sum; hsum = w_high_sum;
    pmin = w_period_min; pmax = w_period_max; hmin = w_high_min; hmax = w_high_max;
    w_edges = w_periods = 0; w_period_sum = w_high_sum = 0;
    w_period_min = UINT32_MAX; w_period_max = 0; w_high_min = UINT32_MAX; w_high_max = 0;
    portEXIT_CRITICAL(&s_mux);

    o->edges = edges; o->periods = periods;
    o->level = gpio_get_level(PIN_CAPTURE);
    if (periods) {
        double mp = (double)psum / periods, mh = (double)hsum / periods;
        o->freq_hz = (double)s_res_hz / mp;
        o->duty_pct = 100.0 * mh / mp;
        double k = 1e7 / s_res_hz; // ticks -> 0.1 us
        o->period_min_us10 = (uint32_t)(pmin * k); o->period_max_us10 = (uint32_t)(pmax * k);
        o->high_min_us10 = (uint32_t)(hmin * k);   o->high_max_us10 = (uint32_t)(hmax * k);
    } else {
        o->freq_hz = 0; o->duty_pct = 0;
        o->period_min_us10 = o->period_max_us10 = o->high_min_us10 = o->high_max_us10 = 0;
    }
}
