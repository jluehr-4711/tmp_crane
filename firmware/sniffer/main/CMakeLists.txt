idf_component_register(SRCS "main.c" "probe_adc.c" "probe_capture.c" "probe_speed.c" "probe_uart.c" "pwm_out.c" "console_cmds.c"
                       INCLUDE_DIRS "."
                       PRIV_REQUIRES console driver esp_adc esp_timer esp_driver_mcpwm esp_driver_ledc esp_driver_gpio esp_driver_uart)
