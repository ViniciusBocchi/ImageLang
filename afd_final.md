# AFD Final (Diagrama Mermaid)

```mermaid
stateDiagram-v2
    [*] --> S0

    S0 --> S_name_start: [A-Za-z_]
    S_name_start --> S_name_start: [A-Za-z0-9_]
    S_name_start --> S_accept_NAME: <<accept NAME>>

    S0 --> S_num_int: [0-9]
    S_num_int --> S_num_int: [0-9]
    S_num_int --> S_num_dot: "."
    S_num_dot --> S_num_frac: [0-9]
    S_num_frac --> S_num_frac: [0-9]
    S_num_int --> S_accept_NUMBER: <<accept NUMBER>>
    S_num_frac --> S_accept_NUMBER: <<accept NUMBER>>

    S0 --> S_quote_dq: "\""
    S0 --> S_quote_sq: "'"
    S_quote_dq --> S_quote_dq: [any except " and \\]
    S_quote_dq --> S_quote_escape_dq: "\\"
    S_quote_escape_dq --> S_quote_dq: any
    S_quote_dq --> S_accept_STRING: "\""
    S_quote_sq --> S_quote_sq: [any except ' and \\]
    S_quote_sq --> S_quote_escape_sq: "\\"
    S_quote_escape_sq --> S_quote_sq: any
    S_quote_sq --> S_accept_STRING: "'"

    S0 --> S_accept_ASSIGN: "="
    S0 --> S_accept_COMMA: ","
    S0 --> S_accept_LSQB: "["
    S0 --> S_accept_RSQB: "]"
    S0 --> S_accept_COLON: ":"
    S0 --> S_accept_LPAREN: "("
    S0 --> S_accept_RPAREN: ")"
    S0 --> S_accept_NEWLINE: "\\n"
