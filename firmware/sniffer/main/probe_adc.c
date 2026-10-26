#include "sniffer.h"
#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali_scheme.h"
#include "esp_log.h"

static const char *TAG = "adc";
static adc_oneshot_unit_handle_t s_unit;
static adc_cali_handle_t s_cali;
static bool s_cali_ok;
static float s_divider = ADC_DIVIDER_DEFAULT;

static const adc_channel_t s_ch[4] = {
    ADC_CHANNEL_6, // GPIO34
    ADC_CHANNEL_7, // GPIO35
    ADC_CHANNEL_4, // GPIO32
    ADC_CHANNEL_5, // GPIO33
};

void probe_adc_init(void)
{
    adc_oneshot_unit_init_cfg_t ucfg = { .unit_id = ADC_UNIT_1 };
    ESP_ERROR_CHECK(adc_oneshot_new_unit(&ucfg, &s_unit));
    adc_oneshot_chan_cfg_t ccfg = {
        .atten = ADC_ATTEN_DB_12,          // ~0..3.1 V usable on the classic ESP32
        .bitwidth = ADC_BITWIDTH_DEFAULT,
    };
    for (int i = 0; i < 4; i++) {
        ESP_ERROR_CHECK(adc_oneshot_config_channel(s_unit, s_ch[i], &ccfg));
    }
    adc_cali_line_fitting_config_t cal = {
        .unit_id = ADC_UNIT_1,
        .atten = ADC_ATTEN_DB_12,
        .bitwidth = ADC_BITWIDTH_DEFAULT,
    };
    s_cali_ok = (adc_cali_create_scheme_line_fitting(&cal, &s_cali) == ESP_OK);
    ESP_LOGI(TAG, "ADC ready, calibration %s, divider %.2f", s_cali_ok ? "ok" : "MISSING (raw*0.8)", s_divider);
}

void probe_adc_set_divider(float ratio) { if (ratio > 0) s_divider = ratio; }
float probe_adc_divider(void) { return s_divider; }

static int raw_to_mv(int raw)
{
    int mv = 0;
    if (s_cali_ok && adc_cali_raw_to_voltage(s_cali, raw, &mv) == ESP_OK) return mv;
    return raw * 3100 / 4095; // crude fallback
}

int probe_adc_read(int mv[4], int min_mv[4], int max_mv[4])
{
    const int N = 64;
    for (int i = 0; i < 4; i++) {
        long sum = 0; int mn = 1 << 30, mx = -1;
        for (int n = 0; n < N; n++) {
            int raw = 0;
            if (adc_oneshot_read(s_unit, s_ch[i], &raw) != ESP_OK) continue;
            int v = raw_to_mv(raw);
            sum += v; if (v < mn) mn = v; if (v > mx) mx = v;
        }
        mv[i] = (int)(sum / N);
        if (min_mv) min_mv[i] = mn;
        if (max_mv) max_mv[i] = mx;
    }
    return N;
}
