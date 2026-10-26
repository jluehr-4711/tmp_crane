// PWM output for the replay test (session 6): reproduce the console's DOUT.
#include "sniffer.h"
#include "driver/ledc.h"
#include "esp_log.h"
#include <math.h>

static const char *TAG = "pwm";
static uint32_t s_freq; static float s_duty; static bool s_inv;

void pwm_out_set_inverted(bool inv) { s_inv = inv; if (s_freq) pwm_out_set(s_freq, s_duty); }
bool pwm_out_inverted(void) { return s_inv; }

void pwm_out_init(void) {}

void pwm_out_set(uint32_t freq_hz, float duty_pct)
{
    if (freq_hz == 0) {
        ledc_stop(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, s_inv ? 1 : 0); // idle = DOUT low
        s_freq = 0; s_duty = 0; ESP_LOGI(TAG, "pwm off, GPIO%d low", PIN_PWM_OUT);
        return;
    }
    if (duty_pct < 0) duty_pct = 0;
    if (duty_pct > 100) duty_pct = 100;
    // pick the finest resolution the LEDC timer allows at this frequency
    uint32_t res_bits = ledc_find_suitable_duty_resolution(80000000, freq_hz);
    if (res_bits == 0) { ESP_LOGE(TAG, "frequency %lu not possible", (unsigned long)freq_hz); return; }
    if (res_bits > 13) res_bits = 13;
    ledc_timer_config_t t = {
        .speed_mode = LEDC_LOW_SPEED_MODE, .timer_num = LEDC_TIMER_0,
        .duty_resolution = (ledc_timer_bit_t)res_bits, .freq_hz = freq_hz, .clk_cfg = LEDC_AUTO_CLK,
    };
    ESP_ERROR_CHECK(ledc_timer_config(&t));
    ledc_channel_config_t c = {
        .gpio_num = PIN_PWM_OUT, .speed_mode = LEDC_LOW_SPEED_MODE, .channel = LEDC_CHANNEL_0,
        .timer_sel = LEDC_TIMER_0, .duty = 0, .hpoint = 0,
    };
    ESP_ERROR_CHECK(ledc_channel_config(&c));
    uint32_t maxd = (1u << res_bits) - 1;
    float eff = s_inv ? 100.0f - duty_pct : duty_pct;   // transistor stage inverts the line
    uint32_t d = (uint32_t)lroundf(eff / 100.0f * maxd);
    ESP_ERROR_CHECK(ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, d));
    ESP_ERROR_CHECK(ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0));
    s_freq = freq_hz; s_duty = duty_pct;
    ESP_LOGI(TAG, "pwm %lu Hz DOUT duty %.2f %% (%lu/%lu on GPIO%d%s)", (unsigned long)freq_hz, duty_pct,
             (unsigned long)d, (unsigned long)maxd, PIN_PWM_OUT, s_inv ? ", inverted" : "");
}

void pwm_out_get(uint32_t *f, float *d) { *f = s_freq; *d = s_duty; }
