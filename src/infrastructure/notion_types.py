from typing import TypedDict, Literal, Required, Any


################# Common types ##################

class NotionPageParent(TypedDict):
    type: Literal["page_id"]
    page_id: str


class NotionDatabaseParent(TypedDict):
    type: Literal["database_id"]
    database_id: str


type NotionParent = NotionPageParent | NotionDatabaseParent


class NotionText(TypedDict):
    content: str
    link: str | None


class NotionRichText(TypedDict):
    type: Literal["text"]
    Text: NotionText
    plain_text: str


class NotionDate(TypedDict, total=False):
    start: Required[str]
    end: str | None
    time_zone: str | None


class NotionStatus(TypedDict, total=False):
    id: str
    name: str
    color: Literal["default", "gray", "brown", "orange", "yellow", "green", "blue", "purple", "pink", "red"]


class NotionHostedFileRef(TypedDict):
    url: str
    expiry_time: str


class NotionHostedFile(TypedDict):
    type: Literal["file"]
    file: NotionHostedFileRef


class NotionExternalFileRef(TypedDict):
    url: str


class NotionExternalFile(TypedDict):
    type: Literal["external"]
    external: NotionExternalFileRef


class NotionUploadedFileRef(TypedDict):
    id: str


class NotionUploadedFile(TypedDict):
    type: Literal["file_upload"]
    file_upload: NotionUploadedFileRef


type NotionFileObject = NotionHostedFile | NotionExternalFile | NotionUploadedFile


class NotionFormulaBooleanResult(TypedDict):
    type: Literal["boolean"]
    boolean: bool


class NotionFormulaDateResult(TypedDict):
    type: Literal["date"]
    date: str


class NotionFormulaNumberResult(TypedDict):
    type: Literal["number"]
    number: int | float


class NotionFormulaStringResult(TypedDict):
    type: Literal["string"]
    string: str


type NotionFormulaResult = (
        NotionFormulaBooleanResult
        | NotionFormulaDateResult
        | NotionFormulaNumberResult
        | NotionFormulaStringResult
)


class NotionMultiSelectOption(TypedDict):
    id: str
    name: str
    color: Literal["blue", "brown", "default", "gray", "green", "orange", "pink", "purple", "red", "yellow"]


class NotionRelationReference(TypedDict):
    id: str


class NotionRollupResult(TypedDict, total=False):
    type: Literal["array", "date", "incomplete", "number", "unsupported"]
    function: Literal[
        "average", "checked", "count", "count_per_group", "count_values", "date_range",
        "earliest_date", "empty", "latest_date", "max", "median", "min", "not_empty",
        "percent_checked", "percent_empty", "percent_not_empty", "percent_per_group",
        "percent_unchecked", "range", "show_original", "show_unique", "sum", "unchecked", "unique"
    ]
    array: list[Any] | None
    date: str | None
    number: int | float | None
    incomplete: dict[str, Any] | None
    unsupported: dict[str, Any] | None


class NotionSelectOption(TypedDict):
    id: str
    name: str
    color: Literal["blue", "brown", "default", "gray", "green", "orange", "pink", "purple", "red", "yellow"]


class NotionUniqueId(TypedDict):
    number: int | float
    prefix: str | None


class NotionVerificationObject(TypedDict):
    state: str
    verified_by: dict[str, Any]  # TODO: define type
    date: str | None


################# Properties ##################


class BaseNotionProperty(TypedDict):
    id: str


class NotionDateProperty(BaseNotionProperty):
    type: Required[Literal["date"]]
    date: NotionDate


class NotionTitleProperty(BaseNotionProperty):
    type: Literal["title"]
    title: list[NotionRichText]


class NotionStatusProperty(BaseNotionProperty):
    type: Literal["status"]
    status: NotionStatus


class NotionCheckboxProperty(BaseNotionProperty):
    type: Literal["checkbox"]
    checkbox: bool


class NotionCreatedByProperty(BaseNotionProperty):
    type: Literal["created_by"]
    created_by: dict[str, Any]  # TODO: define type


class NotionCreatedTimeProperty(BaseNotionProperty):
    type: Literal["created_time"]
    created_time: str


class NotionEmailProperty(BaseNotionProperty):
    type: Literal["email"]
    email: str


class NotionFilesProperty(BaseNotionProperty):
    type: Literal["files"]
    files: list[NotionFileObject]


class NotionFormulaProperty(BaseNotionProperty):
    type: Literal["formula"]
    formula: NotionFormulaResult


class NotionLastEditedTimeProperty(BaseNotionProperty):
    type: Literal["last_edited_time"]
    last_edited_time: str


class NotionLastEditedByProperty(BaseNotionProperty):
    type: Literal["last_edited_by"]
    last_edited_by: dict[str, Any]  # TODO: define type


class NotionMultiSelectProperty(BaseNotionProperty):
    type: Literal["multi_select"]
    multi_select: list[NotionMultiSelectOption]


class NotionNumberProperty(BaseNotionProperty):
    type: Literal["number"]
    number: int | float | None


class NotionPeopleProperty(BaseNotionProperty):
    type: Literal["people"]
    people: list[dict[str, Any]]  # TODO: define type


class NotionPhoneNumberProperty(BaseNotionProperty):
    type: Literal["phone_number"]
    phone_number: str


class NotionRelationProperty(BaseNotionProperty):
    type: Literal["relation"]
    relation: list[NotionRelationReference]
    has_more: bool


class NotionRollupProperty(BaseNotionProperty):
    type: Literal["rollup"]
    rollup: NotionRollupResult


class NotionRichTextProperty(BaseNotionProperty):
    type: Literal["rich_text"]
    rich_text: list[NotionRichText]


class NotionSelectProperty(BaseNotionProperty):
    type: Literal["select"]
    select: NotionSelectOption


class NotionUrlProperty(BaseNotionProperty):
    type: Literal["url"]
    url: str


class NotionUniqueIdProperty(BaseNotionProperty):
    type: Literal["unique_id"]
    unique_id: NotionUniqueId


class NotionVerificationProperty(BaseNotionProperty):
    type: Literal["verification"]
    verification: NotionVerificationObject


type NotionPageProperty = (
        NotionDateProperty
        | NotionTitleProperty
        | NotionStatusProperty
        | NotionCheckboxProperty
        | NotionCreatedByProperty
        | NotionCreatedTimeProperty
        | NotionEmailProperty
        | NotionFilesProperty
        | NotionFormulaProperty
        | NotionLastEditedTimeProperty
        | NotionLastEditedByProperty
        | NotionMultiSelectProperty
        | NotionNumberProperty
        | NotionPeopleProperty
        | NotionPhoneNumberProperty
        | NotionRelationProperty
        | NotionRollupProperty
        | NotionRichTextProperty
        | NotionSelectProperty
        | NotionUrlProperty
        | NotionUniqueIdProperty
        | NotionVerificationProperty
)


################# Page ##################


class NotionPage(TypedDict):
    object: Literal["page"]
    id: str
    created_time: str
    last_edited_time: str
    parent: NotionParent
    in_trash: bool
    properties: dict[str, NotionPageProperty]


################# Blocks ##################


class BaseNotionBlock(TypedDict):
    object: Literal["block"]
    id: str
    created_time: str
    last_edited_time: str
    parent: NotionParent
    has_children: bool
    in_trash: bool


type NotionColor = Literal[
    "default", "gray", "brown", "orange", "yellow", "green", "blue", "purple", "pink", "red",
    "gray_background", "brown_background", "orange_background", "yellow_background", "green_background",
    "blue_background", "purple_background", "pink_background", "red_background"
]


class NotionEmoji(TypedDict):
    type: Literal["emoji"]
    emoji: str


type NotionIcon = NotionFileObject | NotionEmoji


class NotionParagraphBlockContent(TypedDict):
    rich_text: list[NotionRichText]
    color: NotionColor


class NotionParagraphBlock(BaseNotionBlock):
    type: Required[Literal["paragraph"]]
    paragraph: NotionParagraphBlockContent


class NotionHeading1BlockContent(TypedDict):
    rich_text: list[NotionRichText]
    color: NotionColor
    is_toggleable: bool


class NotionHeading1Block(BaseNotionBlock):
    type: Required[Literal["heading_1"]]
    heading_1: NotionHeading1BlockContent


class NotionHeading2BlockContent(TypedDict):
    rich_text: list[NotionRichText]
    color: NotionColor
    is_toggleable: bool


class NotionHeading2Block(BaseNotionBlock):
    type: Required[Literal["heading_2"]]
    heading_2: NotionHeading2BlockContent


class NotionHeading3BlockContent(TypedDict):
    rich_text: list[NotionRichText]
    color: NotionColor
    is_toggleable: bool


class NotionHeading3Block(BaseNotionBlock):
    type: Required[Literal["heading_3"]]
    heading_3: NotionHeading3BlockContent


class NotionBulletedListItemBlockContent(TypedDict):
    rich_text: list[NotionRichText]
    color: NotionColor


class NotionBulletedListItemBlock(BaseNotionBlock):
    type: Required[Literal["bulleted_list_item"]]
    bulleted_list_item: NotionBulletedListItemBlockContent


class NotionNumberedListItemBlockContent(TypedDict):
    rich_text: list[NotionRichText]
    color: NotionColor


class NotionNumberedListItemBlock(BaseNotionBlock):
    type: Required[Literal["numbered_list_item"]]
    numbered_list_item: NotionNumberedListItemBlockContent


class NotionToDoBlockContent(TypedDict):
    rich_text: list[NotionRichText]
    color: NotionColor
    checked: bool


class NotionToDoBlock(BaseNotionBlock):
    type: Required[Literal["to_do"]]
    to_do: NotionToDoBlockContent


class NotionToggleBlockContent(TypedDict):
    rich_text: list[NotionRichText]
    color: NotionColor


class NotionToggleBlock(BaseNotionBlock):
    type: Required[Literal["toggle"]]
    toggle: NotionToggleBlockContent


class NotionCodeBlockContent(TypedDict):
    rich_text: list[NotionRichText]
    caption: list[NotionRichText]
    language: str


class NotionCodeBlock(BaseNotionBlock):
    type: Required[Literal["code"]]
    code: NotionCodeBlockContent


class NotionChildPageBlockContent(TypedDict):
    title: str


class NotionChildPageBlock(BaseNotionBlock):
    type: Required[Literal["child_page"]]
    child_page: NotionChildPageBlockContent


class NotionChildDatabaseBlockContent(TypedDict):
    title: str


class NotionChildDatabaseBlock(BaseNotionBlock):
    type: Required[Literal["child_database"]]
    child_database: NotionChildDatabaseBlockContent


class NotionEmbedBlockContent(TypedDict):
    url: str


class NotionEmbedBlock(BaseNotionBlock):
    type: Required[Literal["embed"]]
    embed: NotionEmbedBlockContent


class NotionMediaBlockContent(TypedDict, total=False):
    type: Required[Literal["file", "external", "file_upload"]]
    file: NotionHostedFileRef
    external: NotionExternalFileRef
    file_upload: NotionUploadedFileRef
    caption: list[NotionRichText]


class NotionImageBlock(BaseNotionBlock):
    type: Required[Literal["image"]]
    image: NotionMediaBlockContent


class NotionVideoBlock(BaseNotionBlock):
    type: Required[Literal["video"]]
    video: NotionMediaBlockContent


class NotionFileBlock(BaseNotionBlock):
    type: Required[Literal["file"]]
    file: NotionMediaBlockContent


class NotionPdfBlock(BaseNotionBlock):
    type: Required[Literal["pdf"]]
    pdf: NotionMediaBlockContent


class NotionAudioBlock(BaseNotionBlock):
    type: Required[Literal["audio"]]
    audio: NotionMediaBlockContent


class NotionBookmarkBlockContent(TypedDict):
    url: str
    caption: list[NotionRichText]


class NotionBookmarkBlock(BaseNotionBlock):
    type: Required[Literal["bookmark"]]
    bookmark: NotionBookmarkBlockContent


class NotionCalloutBlockContent(TypedDict):
    rich_text: list[NotionRichText]
    icon: NotionIcon
    color: NotionColor


class NotionCalloutBlock(BaseNotionBlock):
    type: Required[Literal["callout"]]
    callout: NotionCalloutBlockContent


class NotionQuoteBlockContent(TypedDict):
    rich_text: list[NotionRichText]
    color: NotionColor


class NotionQuoteBlock(BaseNotionBlock):
    type: Required[Literal["quote"]]
    quote: NotionQuoteBlockContent


class NotionEquationBlockContent(TypedDict):
    expression: str


class NotionEquationBlock(BaseNotionBlock):
    type: Required[Literal["equation"]]
    equation: NotionEquationBlockContent


class NotionDividerBlock(BaseNotionBlock):
    type: Required[Literal["divider"]]
    divider: dict[str, Any]


class NotionTableOfContentsBlockContent(TypedDict):
    color: NotionColor


class NotionTableOfContentsBlock(BaseNotionBlock):
    type: Required[Literal["table_of_contents"]]
    table_of_contents: NotionTableOfContentsBlockContent


class NotionBreadcrumbBlock(BaseNotionBlock):
    type: Required[Literal["breadcrumb"]]
    breadcrumb: dict[str, Any]


class NotionColumnListBlock(BaseNotionBlock):
    type: Required[Literal["column_list"]]
    column_list: dict[str, Any]


class NotionColumnBlock(BaseNotionBlock):
    type: Required[Literal["column"]]
    column: dict[str, Any]


class NotionLinkPreviewBlockContent(TypedDict):
    url: str


class NotionLinkPreviewBlock(BaseNotionBlock):
    type: Required[Literal["link_preview"]]
    link_preview: NotionLinkPreviewBlockContent


class NotionSyncedFrom(TypedDict):
    type: Literal["block_id"]
    block_id: str


class NotionSyncedBlockContent(TypedDict):
    synced_from: NotionSyncedFrom | None


class NotionSyncedBlock(BaseNotionBlock):
    type: Required[Literal["synced_block"]]
    synced_block: NotionSyncedBlockContent


class NotionTemplateBlockContent(TypedDict):
    rich_text: list[NotionRichText]


class NotionTemplateBlock(BaseNotionBlock):
    type: Required[Literal["template"]]
    template: NotionTemplateBlockContent


class NotionLinkToPageBlockContent(TypedDict, total=False):
    type: Required[Literal["page_id", "database_id"]]
    page_id: str
    database_id: str


class NotionLinkToPageBlock(BaseNotionBlock):
    type: Required[Literal["link_to_page"]]
    link_to_page: NotionLinkToPageBlockContent


class NotionTableBlockContent(TypedDict):
    table_width: int
    has_column_header: bool
    has_row_header: bool


class NotionTableBlock(BaseNotionBlock):
    type: Required[Literal["table"]]
    table: NotionTableBlockContent


class NotionTableRowBlockContent(TypedDict):
    cells: list[list[NotionRichText]]


class NotionTableRowBlock(BaseNotionBlock):
    type: Required[Literal["table_row"]]
    table_row: NotionTableRowBlockContent


type NotionBlock = (
        NotionParagraphBlock
        | NotionHeading1Block
        | NotionHeading2Block
        | NotionHeading3Block
        | NotionBulletedListItemBlock
        | NotionNumberedListItemBlock
        | NotionToDoBlock
        | NotionToggleBlock
        | NotionCodeBlock
        | NotionChildPageBlock
        | NotionChildDatabaseBlock
        | NotionEmbedBlock
        | NotionImageBlock
        | NotionVideoBlock
        | NotionFileBlock
        | NotionPdfBlock
        | NotionAudioBlock
        | NotionBookmarkBlock
        | NotionCalloutBlock
        | NotionQuoteBlock
        | NotionEquationBlock
        | NotionDividerBlock
        | NotionTableOfContentsBlock
        | NotionBreadcrumbBlock
        | NotionColumnListBlock
        | NotionColumnBlock
        | NotionLinkPreviewBlock
        | NotionSyncedBlock
        | NotionTemplateBlock
        | NotionLinkToPageBlock
        | NotionTableBlock
        | NotionTableRowBlock
)
