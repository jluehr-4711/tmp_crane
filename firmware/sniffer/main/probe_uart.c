// Serial sniff on UART2 RX. Only used if DOUT turns out not to be PWM.
#include "sniffer.h"
#include "driver/uart.h"
#include "esp_log.h"
#include <string.h>

static const char *TAG = "usn";
static int s_baud;            // 0 = off
static bool s_installed;
static uint32_t s_total;

void probe_uart_init(void) {}

void probe_uart_set_baud(int baud)
{
    if (baud <= 0) {
        if (s_installed) { uart_driver_delete(UART_NUM_2); s_installed = false; }
        s_baud = 0; ESP_LOGI(TAG, "uart sniff off");
        return;
    }
    if (!s_installed) {
        uart_config_t cfg = {
            .baud_rate = baud, .data_bits = UART_DATA_8_BITS, .parity = UART_PARITY_DISABLE,
            .stop_bits = UART_STOP_BITS_1, .flow_ctrl = UART_HW_FLOWCTRL_DISABLE, .source_clk = UART_SCLK_DEFAULT,
        };
        ESP_ERROR_CHECK(uart_driver_install(UART_NUM_2, 1024, 0, 0, NULL, 0));
        ESP_ERROR_CHECK(uart_param_config(UART_NUM_2, &cfg));
        ESP_ERROR_CHECK(uart_set_pin(UART_NUM_2, UART_PIN_NO_CHANGE, PIN_UART_RX, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));
        s_installed = true;
    } else {
        ESP_ERROR_CHECK(uart_set_baudrate(UART_NUM_2, baud));
    }
    s_baud = baud; s_total = 0;
    ESP_LOGI(TAG, "uart sniff on GPIO%d at %d baud 8N1", PIN_UART_RX, baud);
}

int probe_uart_baud(void) { return s_baud; }

int probe_uart_take(uint8_t *buf, int max, uint32_t *total)
{
    if (!s_installed) { *total = s_total; return 0; }
    int n = uart_read_bytes(UART_NUM_2, buf, max, 0);
    if (n > 0) s_total += n;
    *total = s_total;
    return n > 0 ? n : 0;
}
