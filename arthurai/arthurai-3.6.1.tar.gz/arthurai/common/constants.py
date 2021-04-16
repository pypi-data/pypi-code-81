class ListableStrEnum:
    """
    This class operates similar to Enum but passes mypy type checking.
    The members are accessed directly rather than by `.name` or `.value`.
    """

    @classmethod
    def list(cls):
        """
        Lists all attributes in alphabetical order
        """
        members = [getattr(cls, attr) for attr in dir(cls)
                   if not callable(getattr(cls, attr)) and not attr.startswith("__")]
        return sorted(members)


class InputType(ListableStrEnum):
    Tabular = "TABULAR"
    Image = "IMAGE"
    NLP = "NLP"


class OutputType(ListableStrEnum):
    Regression = "REGRESSION"
    Multiclass = "MULTICLASS"
    Multilabel = "MULTILABEL"


class ValueType(ListableStrEnum):
    String = "STRING"
    Integer = "INTEGER"
    Float = "FLOAT"
    Image = "IMAGE"
    Boolean = "BOOLEAN"
    Timestamp = "TIMESTAMP"
    Unstructured_Text = "UNSTRUCTURED_TEXT"


class Stage(ListableStrEnum):
    ModelPipelineInput = "PIPELINE_INPUT"
    PredictFunctionInput = "PREDICT_FUNCTION_INPUT"
    PredictedValue = "PREDICTED_VALUE"
    NonInputData = "NON_INPUT_DATA"
    GroundTruth = "GROUND_TRUTH"


class TextDelimiter(ListableStrEnum):
    """ This class contains patterns that can be used
    as text_delimiter for NLP models.

    Definitions:

    NOT_WORD: `'\W+'` Splits on any character that is not a word. Ex:
              "this  is,aaaa,,,,,test!" = ["this", "is", "aaaa", "test", ""]

    WHITESPACE: `'\s+` Splits on whitespace. Ex:
              "this  is,a test! " = ["this", "is,a", "test!", ""]

    COMMA: `","` Splits on a single comma. Ex:
              "this ,is,,a,test" = ["this ", "is", "", "a", "test"]

    COMMA_PLUS: `",+"` Splits on one or more commas. Ex:
              "this ,is,,a,test" = ["this ", "is", "a", "test"]

    PIPE: `"\|"` Splits on a single pipe. Ex:
              "this |is||a|test" = ["this ", "is", "", "a", "test"]

    PIPE_PLUS: `"\|+"` Splits on one or more pipes. Ex:
              "this |is||a|test" = ["this ", "is", "a", "test"]
    """
    NOT_WORD = "\W+"
    WHITESPACE = "\s+"
    COMMA = ","
    COMMA_PLUS = ",+"
    PIPE = "\|"
    PIPE_PLUS = "\|+"


class Enrichment(ListableStrEnum):
    """This class contains constants for the names of enrichments"""
    AnomalyDetection = "anomaly_detection"
    Explainability = "explainability"
