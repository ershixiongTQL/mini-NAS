#ifndef _NAS_IE_UE_RADIO_CAPABILITY_ID_AVAILABILITY_
#define _NAS_IE_UE_RADIO_CAPABILITY_ID_AVAILABILITY_

#include "lte_nas_ie.h"

#define UE_RCIDAV 0

void nas_ie_ue_radio_capability_id_availability_parse(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv);
const char *nas_ie_ue_radio_capability_id_availability_info_id_to_str(unsigned int id);



#endif