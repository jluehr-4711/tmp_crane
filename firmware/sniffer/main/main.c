// Crosstrainer console-link sniffer. Classic ESP32, ESP-IDF 5.x.
// Prints one report line per second with everything seen on the probe pins.
#include "sniffer.h"
#include "esp_console.h"
#include "esp_log.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <stdio.h>

static const char *TAG = "main";

static void report_task(void *arg)
{
    uint8_t ubuf[64];
    int led = 0;
    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(g_report_interval_ms));
        gpio_set_level(PIN_LED, led ^= 1);
        if (!g_report_enabled) continue;

        int mv[4], mn[4], mx[4];
        probe_adc_read(mv, mn, mx);
        float k = probe_adc_divider();

        capture_stats_t c; probe_capture_snapshot(&c);
        speed_stats_t s;   probe_speed_snapshot(&s);
        uint32_t utotal = 0; int un = probe_uart_take(ubuf, sizeof ubuf, &utotal);

        // ADC: averaged input voltage (after the divider), plus min..max of the pin
        printf("ADC A=%.2fV B=%.2fV C=%.2fV D=%.2fV (pin mV min..max A %d..%d) | ",
               mv[0] * k / 1000, mv[1] * k / 1000, mv[2] * k / 1000, mv[3] * k / 1000, mn[0], mx[0]);
        if (c.periods)
            printf("DOUT %.1f Hz duty %.2f%% per %.1f..%.1f us hi %.1f..%.1f us (%lu edges) | ",
                   c.freq_hz, c.duty_pct, c.period_min_us10 / 10.0, c.period_max_us10 / 10.0,
                   c.high_min_us10 / 10.0, c.high_max_us10 / 10.0, (unsigned long)c.edges);
        else
            printf("DOUT static %s (%lu edges) | ", c.level ? "HIGH" : "LOW", (unsigned long)c.edges);
        printf("SPD total %lu +%lu last %lu ms mean %lu ms lvl %d",
               (unsigned long)s.pulses_total, (unsigned long)s.pulses_window,
               (unsigned long)s.last_interval_ms, (unsigned long)s.mean_interval_ms, s.level);
        if (probe_uart_baud()) {
            printf(" | UART@%d total %lu:", probe_uart_baud(), (unsigned long)utotal);
            for (int i = 0; i < un; i++) printf(" %02X", ubuf[i]);
        }
        printf("\n");
    }
}

void app_main(void)
{
    gpio_reset_pin(PIN_LED);
    gpio_set_direction(PIN_LED, GPIO_MODE_OUTPUT);

    probe_adc_init();
    probe_capture_init();
    probe_speed_init(true);
    probe_uart_init();
    pwm_out_init();

    esp_console_repl_t *repl = NULL;
    esp_console_repl_config_t rcfg = ESP_CONSOLE_REPL_CONFIG_DEFAULT();
    rcfg.prompt = "sniff>";
    rcfg.max_cmdline_length = 128;
    esp_console_dev_uart_config_t ucfg = ESP_CONSOLE_DEV_UART_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_console_new_repl_uart(&ucfg, &rcfg, &repl));
    console_cmds_register();

    xTaskCreate(report_task, "report", 4096, NULL, 5, NULL);
    ESP_LOGI(TAG, "sniffer ready; type 'help'");
    ESP_ERROR_CHECK(esp_console_start_repl(repl));
}
