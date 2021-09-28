
EMM_TYPES = {
    "attach request": 0x41,
    "attach accept": 0x42,
    "attach complete": 0x43,
    "attach reject": 0x44,
    "detach request": 0x45,
    "detach accept": 0x46,

    "tracking area update request": 0x48,
    "tracking area update accept": 0x49,
    "tracking area update complete": 0x4a,
    "tracking area update reject": 0x4b,
    
    "extended service request": 0x4c,
    "control plane service request": 0x4d,
    "service reject": 0x4e,
    "service accept": 0x4f,
    
    "guti reallocation command": 0x50,
    "guti reallocation complete": 0x51,
    "authentication request": 0x52,
    "authentication response": 0x53,
    "authentication reject": 0x54,
    "authentication failure": 0x5c,
    "identity request": 0x55,
    "identity response": 0x56,
    "security mode command": 0x5d,
    "security mode complete": 0x5e,
    "security mode reject": 0x5f,
    
    "emm status": 0x60,
    "emm information": 0x61,
    "downlink nas transport": 0x62,
    "uplink nas transport": 0x63,
    "cs service notification": 0x64,
    "downlink generic nas transport": 0x68,
    "uplink generic nas transport": 0x69,
}

ESM_TYPES = {
    "activate default eps bearer context request" : 0xc1,
    "activate default eps bearer context accept" : 0xc2,
    "activate default eps bearer context reject" : 0xc3,

    "activate dedicated eps bearer context request" : 0xc5,
    "activate dedicated eps bearer context accept" : 0xc6,
    "activate dedicated eps bearer context reject" : 0xc7,

    "modify eps bearer context request" : 0xc9,
    "modify eps bearer context accept" : 0xca,
    "modify eps bearer context reject" : 0xcb,

    "deactivate eps bearer context request" : 0xcd,
    "deactivate eps bearer context accept" : 0xce,

    "pdn connectivity request" : 0xd0,
    "pdn connectivity reject" : 0xd1,

    "pdn disconnect request" : 0xd2,
    "pdn disconnect reject" : 0xd3,

    "bearer resource allocation request" : 0xd4,
    "bearer resource allocation reject" : 0xd45,

    "bearer resource modification request" : 0xd6,
    "bearer resource modification reject" : 0xd7,

    "esm information request" : 0xd9,
    "esm information response" : 0xda,

    "notification" : 0xdb,

    "esm dummy message" : 0xdc,

    "esm status" : 0xe8,

    "remote ue report" : 0xe9,
    "remote ue report response" : 0xea,

    "esm data transport" : 0xeb,
}

