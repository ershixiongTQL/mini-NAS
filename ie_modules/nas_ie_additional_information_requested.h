#ifndef _NAS_IE_ADDITIONAL_INFORMATION_REQUESTED_H_
#define _NAS_IE_ADDITIONAL_INFORMATION_REQUESTED_H_

#include "lte_nas_ie.h"

#define CIPHER_KEY 0

void nas_ie_additional_information_requested_parse(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv);
const char *nas_ie_additional_information_requested_info_id_to_str(unsigned int id);

#endif

