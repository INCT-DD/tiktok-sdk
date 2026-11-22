"""Define the region codes and video fields used by the Research API."""

from enum import StrEnum

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, JsonValue


class VideoRegionCode(StrEnum):
    """Enum representing the available region codes for TikTok videos."""

    FR = "FR"
    TH = "TH"
    MM = "MM"
    BD = "BD"
    IT = "IT"
    NP = "NP"
    IQ = "IQ"
    BR = "BR"
    US = "US"
    KW = "KW"
    VN = "VN"
    AR = "AR"
    KZ = "KZ"
    GB = "GB"
    UA = "UA"
    TR = "TR"
    ID = "ID"
    PK = "PK"
    NG = "NG"
    KH = "KH"
    PH = "PH"
    EG = "EG"
    QA = "QA"
    MY = "MY"
    ES = "ES"
    JO = "JO"
    MA = "MA"
    SA = "SA"
    TW = "TW"
    AF = "AF"
    EC = "EC"
    MX = "MX"
    BW = "BW"
    JP = "JP"
    LT = "LT"
    TN = "TN"
    RO = "RO"
    LY = "LY"
    IL = "IL"
    DZ = "DZ"
    CG = "CG"
    GH = "GH"
    DE = "DE"
    BJ = "BJ"
    SN = "SN"
    SK = "SK"
    BY = "BY"
    NL = "NL"
    LA = "LA"
    BE = "BE"
    DO = "DO"
    TZ = "TZ"
    LK = "LK"
    NI = "NI"
    LB = "LB"
    IE = "IE"
    RS = "RS"
    HU = "HU"
    PT = "PT"
    GP = "GP"
    CM = "CM"
    HN = "HN"
    FI = "FI"
    GA = "GA"
    BN = "BN"
    SG = "SG"
    BO = "BO"
    GM = "GM"
    BG = "BG"
    SD = "SD"
    TT = "TT"
    OM = "OM"
    FO = "FO"
    MZ = "MZ"
    ML = "ML"
    UG = "UG"
    RE = "RE"
    PY = "PY"
    GT = "GT"
    CI = "CI"
    SR = "SR"
    AO = "AO"
    AZ = "AZ"
    LR = "LR"
    CD = "CD"
    HR = "HR"
    SV = "SV"
    MV = "MV"
    GY = "GY"
    BH = "BH"
    TG = "TG"
    SL = "SL"
    MK = "MK"
    KE = "KE"
    MT = "MT"
    MG = "MG"
    MR = "MR"
    PA = "PA"
    IS = "IS"
    LU = "LU"
    HT = "HT"
    TM = "TM"
    ZM = "ZM"
    CR = "CR"
    NO = "NO"
    AL = "AL"
    ET = "ET"
    GW = "GW"
    AU = "AU"
    KR = "KR"
    UY = "UY"
    JM = "JM"
    DK = "DK"
    AE = "AE"
    MD = "MD"
    SE = "SE"
    MU = "MU"
    SO = "SO"
    CO = "CO"
    AT = "AT"
    GR = "GR"
    UZ = "UZ"
    CL = "CL"
    GE = "GE"
    PL = "PL"
    CA = "CA"
    CZ = "CZ"
    ZA = "ZA"
    AI = "AI"
    VE = "VE"
    KG = "KG"
    PE = "PE"
    CH = "CH"
    LV = "LV"
    PR = "PR"
    NZ = "NZ"
    TL = "TL"
    BT = "BT"
    MN = "MN"
    FJ = "FJ"
    SZ = "SZ"
    VU = "VU"
    BF = "BF"
    TJ = "TJ"
    BA = "BA"
    AM = "AM"
    TD = "TD"
    SI = "SI"
    CY = "CY"
    MW = "MW"
    EE = "EE"
    XK = "XK"
    ME = "ME"
    KY = "KY"
    YE = "YE"
    LS = "LS"
    ZW = "ZW"
    MC = "MC"
    GN = "GN"
    BS = "BS"
    PF = "PF"
    NA = "NA"
    VI = "VI"
    BB = "BB"
    BZ = "BZ"
    CW = "CW"
    PS = "PS"
    FM = "FM"
    PG = "PG"
    BI = "BI"
    AD = "AD"
    TV = "TV"
    GL = "GL"
    KM = "KM"
    AW = "AW"
    TC = "TC"
    CV = "CV"
    MO = "MO"
    VC = "VC"
    NE = "NE"
    WS = "WS"
    MP = "MP"
    DJ = "DJ"
    RW = "RW"
    AG = "AG"
    GI = "GI"
    GQ = "GQ"
    AS = "AS"
    AX = "AX"
    TO = "TO"
    KN = "KN"
    LC = "LC"
    NC = "NC"
    LI = "LI"
    SS = "SS"
    IR = "IR"
    SY = "SY"
    IM = "IM"
    SC = "SC"
    VG = "VG"
    SB = "SB"
    DM = "DM"
    KI = "KI"
    UM = "UM"
    SX = "SX"
    GD = "GD"
    MH = "MH"
    BQ = "BQ"
    YT = "YT"
    ST = "ST"
    CF = "CF"
    BM = "BM"
    SM = "SM"
    PW = "PW"
    GU = "GU"
    HK = "HK"
    IN = "IN"
    CK = "CK"
    AQ = "AQ"
    WF = "WF"
    JE = "JE"
    MQ = "MQ"
    CN = "CN"
    GF = "GF"
    MS = "MS"
    GG = "GG"
    TK = "TK"
    FK = "FK"
    PM = "PM"
    NU = "NU"
    MF = "MF"
    ER = "ER"
    NF = "NF"
    VA = "VA"
    IO = "IO"
    SH = "SH"
    BL = "BL"
    CU = "CU"
    NR = "NR"
    TP = "TP"
    BV = "BV"
    EH = "EH"
    PN = "PN"
    TF = "TF"
    RU = "RU"


class VideoMetadata(BaseModel):
    """Keep additional JSON properties when TikTok adds fields to a video object."""

    model_config = ConfigDict(extra="allow")
    __pydantic_extra__: dict[str, JsonValue] = Field(init=False)


class HashtagInfo(VideoMetadata):
    """Identify a hashtag and give its description when available."""

    hashtag_id: int | str | None = None
    hashtag_name: str | None = None
    hashtag_description: str | None = None


class StickerInfo(VideoMetadata):
    """Identify an interactive sticker in a video."""

    sticker_id: int | str | None = None
    sticker_name: str | None = None


class EffectInfo(VideoMetadata):
    """Describe a video effect and its image, using either API spelling for the URL."""

    effect_id: int | str | None = None
    effect_name: str | None = None
    effect_photo_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("effect_photo_url", "effect_photo_URI"),
    )


class VideoLabel(VideoMetadata):
    """Store the label text, type code, and flags supplied for the video."""

    content: str | None = None
    sink: bool | None = None
    type: int | None = None
    vote: bool | None = None
    warn: bool | None = None


class VideoTag(VideoMetadata):
    """Keep the original tag keys and codes from search results and user video lists.

    The two references assign different meanings to the same numeric codes.
    Use the field names and values from the endpoint that produced the record.
    """

    type: str | int | None = None
    number: int | str | None = None
    video_tag_type: str | int | None = None
    video_tag_number: int | str | None = None


class VideoRecord(VideoMetadata):
    """Store video fields available in search results and user video lists.

    Each field is optional because callers select the fields they need. TikTok
    describes the metadata fields as structures. Keep a single object or a list
    as received. A returned video ID is available as ``id`` with either wire key.
    """

    id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("id", "video_id"),
        description="The unique ID of the video.",
    )
    create_time: int | None = Field(
        default=None, description="Video creation time in UTC seconds."
    )
    username: str | None = Field(
        default=None, description="Username of the video creator."
    )
    region_code: str | None = Field(
        default=None, description="Country where the creator registered the account."
    )
    video_description: str | None = None
    music_id: int | None = None
    like_count: int | None = None
    comment_count: int | None = None
    share_count: int | None = None
    view_count: int | None = None
    hashtag_names: list[str] | None = None
    is_stem_verified: bool | None = Field(
        default=None, description="Whether TikTok verified the video as STEM content."
    )
    video_duration: int | None = Field(
        default=None, description="Video duration in seconds."
    )
    favorites_count: int | None = Field(
        default=None,
        validation_alias=AliasChoices("favorites_count", "favourites_count"),
        description="Number of times the video was saved as a favorite.",
    )
    hashtag_info_list: list[HashtagInfo] | HashtagInfo | None = None
    sticker_info_list: list[StickerInfo] | StickerInfo | None = None
    effect_info_list: list[EffectInfo] | EffectInfo | None = None
    video_mention_list: list[str] | None = None
    video_label: VideoLabel | list[VideoLabel] | None = None
    video_tag: VideoTag | list[VideoTag] | None = None
