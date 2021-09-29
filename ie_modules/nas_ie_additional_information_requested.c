#include "nas_ie_additional_information_requested.h"

#include "nas_ie_additional_information_requested_info_enable.h"

struct additional_information_requested{
	union{
		unsigned char octet;
		struct{
#if __BYTE_ORDER == __BIG_ENDIAN
			unsigned char cipher_key : 1,
						  spare : 7;
#else
			unsigned char spare : 7,
						  cipher_key : 1;
#endif
			}m;
		}u;
};


static void parse(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv){

	struct additional_information_requested *ie = (struct additional_information_requested *)data;

#ifdef CARE_ADDITIONAL_INFORMATION_REQUESTED_CIPHER_KEY
	noticer((unsigned int)CIPHER_KEY, (unsigned char *)&(ie->u.octet), len, priv);
#endif
}

void nas_ie_additional_information_requested_parse(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv)
{
	parse(data, len, noticer, priv);
}


const char *nas_ie_additional_information_requested_info_id_to_str(unsigned int id)
{

	if(id == CIPHER_KEY)
		return "CIPHER_KEY";
	return "?";
}





