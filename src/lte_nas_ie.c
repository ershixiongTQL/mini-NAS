#include "lte_nas_ie.h"


void ie_info_noticer(unsigned int info_id, unsigned char *info, unsigned short len, void *priv){
	struct nas_msg_noticer_priv *private = (struct nas_msg_noticer_priv *)priv;
	private->noticer(private->msg_id, private->msg_ie_id, info_id, info, len);
}
