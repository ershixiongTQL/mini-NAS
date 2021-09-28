#ifndef _LTE_NAS_TRACKING_AREA_IDENTITY_H_
#define _LTE_NAS_TRACKING_AREA_IDENTITY_H_

#include "lte_nas_ie.h"

typedef enum lte_nas_tracking_area_identity_info_e{
    MCC,
    MNC,
    TAC,
}lte_nas_tracking_area_identity_info_t;

void nas_ie_tracking_area_identity_parse(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv);
const char *nas_ie_tracking_area_identity_info_id_to_str(unsigned int id);

#endif