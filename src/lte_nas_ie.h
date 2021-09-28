#ifndef _LTE_NAS_IE_H_
#define _LTE_NAS_IE_H_

#include <winsock.h>
#include <stdio.h>
#include <string.h>

typedef enum{
    PRESENCE_MANDATORY,
    PRESENCE_OPTIONAL,
    PRESENCE_CONDITIONAL,
}lte_ie_presence_t;

typedef enum {
    TRACKING_AREA_IDENTITY, //TS 24.301 9.9.3.32
}lte_ie_t;

struct ie_hdr_tlv{
    unsigned char t;
    unsigned char l;
};

struct ie_hdr_tv{
    unsigned char t;
};

struct ie_hdr_lv{
    unsigned char l;
};

struct ie_hdr_tlv_e{
    unsigned char t;
    unsigned short l;
};

// struct ie_hdr_tv{
//     unsigned char t;
// };

struct ie_hdr_lv_e{
    unsigned short l;
};

typedef unsigned int lte_nas_msg_t;

typedef void (*lte_nas_ie_info_noticer)(unsigned int info_id, unsigned char *info, unsigned short len, void *priv);
typedef void (*lte_nas_msg_noticer)(lte_nas_msg_t msg_type, unsigned int msg_ie_id, unsigned int info_id, unsigned char *info, unsigned short len);
typedef void (*lte_nas_ie_parser)(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv);

struct nas_msg_noticer_priv{
    lte_nas_msg_noticer noticer;

    unsigned msg_id;
    unsigned msg_ie_id;
    unsigned msg_ie_info_id;
};

#endif