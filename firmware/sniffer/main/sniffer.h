// Sniffer firmware: characterises the signals on the crosstrainer console link
// (4-pin "SENSOR"/"CONNECTOR" plug: 5V, GND, DOUT, speed) with a classic ESP32.
// See docs/07-sniffer.md for the pin map and the voltage dividers. Nothing above
// 3.3 V may reach an ESP32 pin.
#pragma once
#include <stdint.h>
#include <stdbool.h>

// ---- pin map (classic ESP32 DevKit) ----
#define PIN_ADC_A      34   // ADC1_CH6, input only  (probe A, e.g. the 5V line via 100k/10k)
#define PIN_ADC_B      35   // ADC1_CH7, input only  (probe B)
#define PIN_ADC_C      32   // ADC1_CH4              (probe C)
#define PIN_ADC_D      33   // ADC1_CH5              (probe D)
#define PIN_CAPTURE    25   // MCPWM capture input: DOUT (via 10k/15k divider)
#define PIN_SPEED      26   // speed pulse input (internal pull-up selectable)
#define PIN_UART_RX    16   // UART2 RX for the serial-sniff mode (via divider)
#define PIN_PWM_OUT    27   // LEDC PWM output for the replay test
#define PIN_LED         2   // on-board LED heartbeat

// Divider ratio applied to the ADC probes: V_in = V_pin * ADC_DIVIDER.
// 100k (top) / 10k (bottom) -> 11.0. Change with the "div" console command.
#define ADC_DIVIDER_DEFAULT 11.0f

// ---- ADC probes ----
void probe_adc_init(void);
void probe_adc_set_divider(float ratio);
// Fill mv[4] with the averaged pin voltage in millivolts (before the divider),
// min_mv/max_mv optional. Returns number of samples taken.
int  probe_adc_read(int mv[4], int min_mv[4], int max_mv[4]);
float probe_adc_divider(void);

// ---- DOUT capture (MCPWM, both edges, 80 MHz timestamps) ----
typedef struct {
    uint32_t edges;         // edges seen in the window
    uint32_t periods;       // complete rising-to-rising periods measured
    double   freq_hz;       // 1 / mean period
    double   duty_pct;      // mean high time / mean period * 100
    uint32_t period_min_us10; // min period in 0.1 us units
    uint32_t period_max_us10;
    uint32_t high_min_us10;
    uint32_t high_max_us10;
    int      level;         // current pin level when idle
} capture_stats_t;
void probe_capture_init(void);
void probe_capture_snapshot(capture_stats_t *out); // reads and resets the window

// ---- speed pulse (GPIO interrupt, ms timestamps) ----
typedef struct {
    uint32_t pulses_total;
    uint32_t pulses_window;
    uint32_t last_interval_ms;  // between the last two pulses
    uint32_t mean_interval_ms;  // over the window
    int      level;
} speed_stats_t;
void probe_speed_init(bool pullup);
void probe_speed_set_pullup(bool pullup);
void probe_speed_snapshot(speed_stats_t *out);

// ---- UART sniff ----
void probe_uart_init(void);
void probe_uart_set_baud(int baud);   // 0 = off
int  probe_uart_baud(void);
// Copies up to max bytes received since the last call; returns count, sets *total.
int  probe_uart_take(uint8_t *buf, int max, uint32_t *total);

// ---- PWM out (replay test) ----
void pwm_out_init(void);
void pwm_out_set(uint32_t freq_hz, float duty_pct); // freq 0 = off
void pwm_out_get(uint32_t *freq_hz, float *duty_pct);

// ---- console / reporting ----
void console_cmds_register(void);
extern volatile bool g_report_enabled;
extern volatile int  g_report_interval_ms;
