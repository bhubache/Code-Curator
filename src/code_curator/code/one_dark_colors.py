from pygments.style import Style

from pygments.token import Keyword, Name, Comment, String, Error, Text, \
     Number, Operator, Generic, Whitespace, Punctuation, Other, Literal

# TODO:
#  1. Highlighting for punctuation in type hints
#  2. Semantic highlighting of parameters

from manim import RED
from manim import YELLOW

class OneDarkStyle(Style):

    background_color = "#272822"
    highlight_color = "#49483e"

    styles = {
        # No corresponding class for the following:
        # Text:                      "#f8f8f2", # class:  ''
        Text:                      "#282c34", # class:  ''
        Whitespace:                "",        # class: 'w'
        Error:                     "#960050 bg:#1e0010", # class: 'err'
        Other:                     "",        # class 'x'

        # Comment:                   "#75715e", # class: 'c'
        Comment:                   "#5c6370", # class: 'c'
        Comment.Multiline:         "",        # class: 'cm'
        Comment.Preproc:           "",        # class: 'cp'
        Comment.Single:            "",        # class: 'c1'
        Comment.Special:           "",        # class: 'cs'

        # Keyword:                   "#66d9ef", # class: 'k'
        Keyword:                   "#c678dd", # class: 'k'
        Keyword.Constant:          "",        # class: 'kc'
        Keyword.Declaration:       "",        # class: 'kd'
        # Keyword.Namespace:         "#f92672", # class: 'kn'
        Keyword.Namespace:         "", # class: 'kn'
        Keyword.Pseudo:            "",        # class: 'kp'
        Keyword.Reserved:          "",        # class: 'kr'
        Keyword.Type:              "",        # class: 'kt'

        # Operator:                  "#f92672", # class: 'o'
        Operator:                  "", # class: 'o'
        Operator.Word:             "#c678dd",        # class: 'ow' - like keywords

        # Punctuation:               "#f8f8f2", # class: 'p'
        # Punctuation: "#353940",  # class: 'p'
        # Punctuation:               "#e5c07b", # class: 'p'

        # Name:                      "#f8f8f2", # class: 'n'
        # Name:                      "#61afef", # class: 'n'
        Name: "#FFFFFF",
        Name.Attribute:            "",
        Name.Builtin:              "#56b6c2",
        Name.Builtin.Pseudo:       "#c678dd",
        Name.Class:                 "#e5c07b",
        Name.Constant:              "#d19a66",
        Name.Decorator: "#e5c07b",
        Name.Entity: YELLOW,
        Name.Exception: "#56b6c2",
        Name.Function: "#61afef",
        Name.Property: YELLOW,
        Name.Label: YELLOW,
        Name.Namespace: "",
        Name.Other: YELLOW,
        Name.Tag: YELLOW,
        Name.Variable: YELLOW,
        Name.Variable.Class: YELLOW,
        Name.Variable.Global: YELLOW,
        Name.Variable.Instance: YELLOW,
        Name.Variable.Magic: YELLOW,


        # Name.Attribute:            "#61afef", # class: 'na' - to be revised
        # Name.Builtin:              "#56b6c2",        # class: 'nb'
        # Name.Builtin.Pseudo:       "#c678dd",        # class: 'bp'
        # Name.Class:                "#e5c07b", # class: 'nc' - to be revised
        # Name.Constant:             "#d19a66", # class: 'no' - to be revised
        # Name.Decorator:            "#e5c07b", # class: 'nd' - to be revised
        # Name.Entity:               "#e06c75",        # class: 'ni'
        # Name.Exception:            "#a6e22e", # class: 'ne'
        # Name.Function:             "#61afef", # class: 'nf'
        # # Name.Property:             "#61afef",        # class: 'py'
        # # Name.Label:                "#c678dd",        # class: 'nl'
        # # Name.Other:                "#a6e22e", # class: 'nx'
        # # Name.Tag:                  "#f92672", # class: 'nt' - like a keyword
        # # Name.Variable:             "#abb2bf",        # class: 'nv' - to be revised
        # Name.Variable:             "#61afef",        # class: 'nv' - to be revised
        # Name.Variable.Class:       "#61afef",        # class: 'vc' - to be revised
        # Name.Variable.Global:      "#e06c75",        # class: 'vg' - to be revised
        # Name.Variable.Instance:    "#61afef",        # class: 'vi' - to be revised

        # Number:                    "#ae81ff", # class: 'm'
        Number:                    "#d19a66", # class: 'm'
        Number.Float:              "",        # class: 'mf'
        Number.Hex:                "",        # class: 'mh'
        Number.Integer:            "",        # class: 'mi'
        Number.Integer.Long:       "",        # class: 'il'
        Number.Oct:                "",        # class: 'mo'

        Literal:                   "#ae81ff", # class: 'l'
        Literal.Date:              "#e6db74", # class: 'ld'

        # String:                    "#e6db74", # class: 's'
        String:                    "#98c379", # class: 's'
        String.Backtick:           "",        # class: 'sb'
        String.Char:               "",        # class: 'sc'
        String.Doc:                "",        # class: 'sd' - like a comment
        String.Double:             "",        # class: 's2'
        # String.Escape:             "#ae81ff", # class: 'se'
        String.Escape:             "#56b6c2", # class: 'se'
        String.Heredoc:            "",        # class: 'sh'
        String.Interpol:           "",        # class: 'si'
        String.Other:              "",        # class: 'sx'
        String.Regex:              "",        # class: 'sr'
        String.Single:             "",        # class: 's1'
        String.Symbol:             "",        # class: 'ss'


        # Generic:                   "",        # class: 'g'
        # Generic.Deleted:           "#f92672", # class: 'gd',
        # Generic.Emph:              "italic",  # class: 'ge'
        # Generic.Error:             "",        # class: 'gr'
        # Generic.Heading:           "",        # class: 'gh'
        # Generic.Inserted:          "#a6e22e", # class: 'gi'
        # Generic.Output:            "#66d9ef", # class: 'go'
        # Generic.Prompt:            "bold #f92672", # class: 'gp'
        # Generic.Strong:            "bold",    # class: 'gs'
        # Generic.Subheading:        "#75715e", # class: 'gu'
        # Generic.Traceback:         "",        # class: 'gt'
    }
