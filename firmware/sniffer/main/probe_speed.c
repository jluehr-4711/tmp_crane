// Speed pulse input: slow signal (a few Hz), GPIO interrupt on the falling edge
// with a 5 ms debounce (reed contacts bounce).
#include "sniffer.h"
#include "driver/gpio.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "esp_log.h"

static const char *TAG = "spd";
static portMUX_TYPE s_mux = portMUX_INITIALIZER_UNLOCKED;
static volatile uint32_t s_total, s_window;
static volatile uint64_t s_sum_us;
static volatile uint32_t s_last_interval_us;
static int64_t s_last_us;

static void IRAM_ATTR on_fall(void *arg)
{
    int64_t now = esp_timer_get_time();
    int64_t d = now - s_last_us;
    if (d < 5000) return;              // debounce 5 ms
    if (s_last_us) {
        s_last_interval_us = (uint32_t)d;
        s_sum_us += d;
    }
    s_last_us = now;
    s_total++; s_window++;
}

void probe_speed_init(bool pullup)
{
    gpio_config_t io = {
        .pin_bit_mask = 1ULL << PIN_SPEED,
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = pullup ? GPIO_PULLUP_ENABLE : GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_NEGEDGE,
    };
    ESP_ERROR_CHECK(gpio_config(&io));
    gpio_install_isr_service(0);
    ESP_ERROR_CHECK(gpio_isr_handler_add(PIN_SPEED, on_fall, NULL));
    ESP_LOGI(TAG, "speed input on GPIO%d, pull-up %s", PIN_SPEED, pullup ? "on" : "off");
}

void probe_speed_set_pullup(bool pullup)
{
    if (pullup) gpio_pullup_en(PIN_SPEED); else gpio_pullup_dis(PIN_SPEED);
}

void probe_speed_snapshot(speed_stats_t *o)
{
    uint32_t total, win, last; uint64_t sum;
    portENTER_CRITICAL(&s_mux);
    total = s_total; win = s_window; last = s_last_interval_us; sum = s_sum_us;
    s_window = 0; s_sum_us = 0;
    portEXIT_CRITICAL(&s_mux);
    o->pulses_total = total; o->pulses_window = win;
    o->last_interval_ms = last / 1000;
    o->mean_interval_ms = win ? (uint32_t)(sum / win / 1000) : 0;
    o->level = gpio_get_level(PIN_SPEED);
}
