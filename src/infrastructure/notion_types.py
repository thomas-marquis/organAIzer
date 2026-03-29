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


################# Bloc ##################


class BaseNotionBlock(TypedDict):
    object: Literal["block"]
    id: str
    created_time: str
    last_edited_time: str
    parent: NotionParent
    has_children: bool
    in_trash: bool
