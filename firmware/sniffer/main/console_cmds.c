// Serial console (115200 8N1 on the USB port). Type "help".
#include "sniffer.h"
#include "esp_console.h"
#include "esp_log.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

volatile bool g_report_enabled = true;
volatile int  g_report_interval_ms = 1000;

static int cmd_report(int argc, char **argv)
{
    if (argc < 2) { printf("report %s every %d ms\n", g_report_enabled ? "on" : "off", g_report_interval_ms); return 0; }
    if (!strcmp(argv[1], "on")) g_report_enabled = true;
    else if (!strcmp(argv[1], "off")) g_report_enabled = false;
    else { int ms = atoi(argv[1]); if (ms >= 100) g_report_interval_ms = ms; else printf("min 100 ms\n"); }
    return 0;
}

static int cmd_div(int argc, char **argv)
{
    if (argc < 2) { printf("adc divider = %.3f (V_in = V_pin * divider)\n", probe_adc_divider()); return 0; }
    probe_adc_set_divider(strtof(argv[1], NULL));
    printf("adc divider = %.3f\n", probe_adc_divider());
    return 0;
}

static int cmd_pullup(int argc, char **argv)
{
    if (argc < 2) { printf("usage: pullup on|off  (internal ~45k pull-up on the speed input GPIO%d)\n", PIN_SPEED); return 0; }
    probe_speed_set_pullup(!strcmp(argv[1], "on"));
    printf("speed pull-up %s\n", argv[1]);
    return 0;
}

static int cmd_uart(int argc, char **argv)
{
    if (argc < 2) { printf("uart sniff: %d baud (0 = off). usage: uart <baud>|off\n", probe_uart_baud()); return 0; }
    probe_uart_set_baud(!strcmp(argv[1], "off") ? 0 : atoi(argv[1]));
    return 0;
}

static int cmd_pwm(int argc, char **argv)
{
    if (argc < 2) {
        uint32_t f; float d; pwm_out_get(&f, &d);
        printf("pwm out on GPIO%d: %lu Hz %.2f %%  usage: pwm <freq_hz> <duty_pct> | pwm off\n", PIN_PWM_OUT, (unsigned long)f, d);
        return 0;
    }
    if (!strcmp(argv[1], "off")) { pwm_out_set(0, 0); return 0; }
    if (argc < 3) { printf("usage: pwm <freq_hz> <duty_pct>\n"); return 1; }
    pwm_out_set((uint32_t)atoi(argv[1]), strtof(argv[2], NULL));
    return 0;
}

static int cmd_pins(int argc, char **argv)
{
    printf("ADC A GPIO%d  ADC B GPIO%d  ADC C GPIO%d  ADC D GPIO%d  (via divider, see 'div')\n", PIN_ADC_A, PIN_ADC_B, PIN_ADC_C, PIN_ADC_D);
    printf("DOUT capture GPIO%d   speed GPIO%d   uart-sniff RX GPIO%d   pwm out GPIO%d\n", PIN_CAPTURE, PIN_SPEED, PIN_UART_RX, PIN_PWM_OUT);
    printf("Never connect more than 3.3 V to any ESP32 pin.\n");
    return 0;
}

void console_cmds_register(void)
{
    const esp_console_cmd_t cmds[] = {
        { .command = "report", .help = "report on|off|<ms>  periodic one-line report", .func = cmd_report },
        { .command = "div",    .help = "div [ratio]  ADC input divider ratio (default 11 = 100k/10k)", .func = cmd_div },
        { .command = "pullup", .help = "pullup on|off  internal pull-up on the speed input", .func = cmd_pullup },
        { .command = "uart",   .help = "uart <baud>|off  sniff serial data on the UART RX pin", .func = cmd_uart },
        { .command = "pwm",    .help = "pwm <freq> <duty%>|off  PWM output for the replay test", .func = cmd_pwm },
        { .command = "pins",   .help = "show the pin map", .func = cmd_pins },
    };
    for (size_t i = 0; i < sizeof(cmds) / sizeof(cmds[0]); i++) ESP_ERROR_CHECK(esp_console_cmd_register(&cmds[i]));
    esp_console_register_help_command();
}
