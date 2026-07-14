# Ruleset

All rules are the production catalog of Quality Clouds Hub (global, active, deterministic — Semgrep or regex). Total: 295 rules.

| Rule | Name | Impact area | Severity | Engine | Tool |
|---|---|---|---|---|---|
| fa-arch-circular-import | Circular import from main | architecture | MEDIUM | semgrep | fastapi |
| fa-arch-db-in-route | DB session in route | architecture | HIGH | semgrep | fastapi |
| fa-arch-exception-handler-broad | Broad exception handler | architecture | MEDIUM | semgrep | fastapi |
| fa-arch-logic-in-route | Business logic in route | architecture | HIGH | semgrep | fastapi |
| fa-arch-manual-response | Manual response construction | architecture | MEDIUM | semgrep | fastapi |
| fa-mng-add-api-route | app.add_api_route usage | manageability | LOW | semgrep | fastapi |
| fa-mng-dict-response | Route returns raw dict | manageability | MEDIUM | semgrep | fastapi |
| fa-mng-hardcoded-config | Hardcoded config in route | manageability | MEDIUM | semgrep | fastapi |
| fa-mng-no-deprecated-marker | Missing deprecated marker | manageability | LOW | semgrep | fastapi |
| fa-mng-no-openapi-tags | App missing openapi_tags | manageability | LOW | semgrep | fastapi |
| fa-mng-no-status-code | Route missing status_code | manageability | MEDIUM | semgrep | fastapi |
| fa-mng-positional-status | Positional status in HTTPException | manageability | LOW | semgrep | fastapi |
| fa-mng-raw-cookie | Raw cookie dict access | manageability | MEDIUM | semgrep | fastapi |
| fa-mnt-magic-status-int | Magic HTTP status integer | maintainability | LOW | semgrep | fastapi |
| fa-mnt-no-summary | Route missing summary | maintainability | LOW | semgrep | fastapi |
| fa-mnt-no-typing-param | Untyped route parameter | maintainability | MEDIUM | semgrep | fastapi |
| fa-prf-blocking-requests | Blocking HTTP call in async route | performance | HIGH | semgrep | fastapi |
| fa-prf-file-open-sync | Sync file open in async handler | performance | HIGH | semgrep | fastapi |
| fa-prf-json-manual | Manual json.dumps in route | performance | MEDIUM | semgrep | fastapi |
| fa-prf-no-streaming | Large response without StreamingResponse | performance | HIGH | semgrep | fastapi |
| fa-prf-on-event-deprecated | Deprecated @app.on_event | performance | MEDIUM | semgrep | fastapi |
| fa-scl-global-state | Mutable global state | scalability | HIGH | semgrep | fastapi |
| fa-scl-hardcoded-workers | Hardcoded uvicorn workers | scalability | MEDIUM | semgrep | fastapi |
| fa-scl-no-pagination | List endpoint without pagination | scalability | HIGH | semgrep | fastapi |
| fa-scl-raw-exception | Raw Exception in route | scalability | HIGH | semgrep | fastapi |
| fa-scl-sync-depends-io | Sync Depends with I/O | scalability | HIGH | semgrep | fastapi |
| fa-scl-sync-middleware | Synchronous middleware | scalability | HIGH | semgrep | fastapi |
| fa-sec-cookie-no-httponly | Cookie missing httponly | security | HIGH | semgrep | fastapi |
| fa-sec-cookie-no-secure | Cookie missing secure flag | security | HIGH | semgrep | fastapi |
| fa-sec-cors-wildcard | CORS allow all origins | security | HIGH | semgrep | fastapi |
| fa-sec-debug-mode | Debug mode enabled | security | HIGH | semgrep | fastapi |
| fa-sec-header-injection | Header set from request data | security | HIGH | semgrep | fastapi |
| fa-sec-path-traversal | Path traversal via user input | security | HIGH | semgrep | fastapi |
| js-console-log-only | console.log Used Instead of Structured Logging | manageability | MEDIUM | semgrep | javascript |
| js-cookie-no-httponly | Missing HttpOnly flag in cookie | security | MEDIUM | semgrep | javascript |
| js-deeply-nested-conditional | Deeply nested conditional | maintainability | MEDIUM | semgrep | javascript |
| js-empty-catch-block | Empty Catch Block Swallows Errors | manageability | HIGH | semgrep | javascript |
| js-eval-usage | eval() or new Function() Dynamic Code Execution | security | HIGH | semgrep | javascript |
| js-fetch-credentials-include | fetch() With credentials:include Without CSRF Protection | security | HIGH | semgrep | javascript |
| js-fetch-no-timeout | Network Request Without Timeout | performance | MEDIUM | semgrep | javascript |
| js-for-in-array | for...in used to iterate an array | performance | MEDIUM | regex | javascript |
| js-function-in-loop | Function defined inside a loop | performance | MEDIUM | semgrep | javascript |
| js-inner-html-assignment | Direct innerHTML / outerHTML Assignment | security | HIGH | semgrep | javascript |
| js-layout-thrashing | Layout thrashing (interleaved DOM read/write) | performance | MEDIUM | semgrep | javascript |
| js-localstorage-token | Sensitive token stored in localStorage | security | HIGH | semgrep | javascript |
| js-mng-loopback-url | Hardcoded Loopback API URL | manageability | HIGH | semgrep | javascript |
| js-mnt-double-negation | Implicit Boolean Coercion via Double Negation | maintainability | LOW | semgrep | javascript |
| js-nested-linear-search | Nested linear search (O(n^2) lookup) | scalability | HIGH | semgrep | javascript |
| js-nested-ternary | Nested ternary expression | maintainability | MEDIUM | semgrep | javascript |
| js-no-document-write | Avoid document.write() | security | HIGH | semgrep | javascript |
| js-no-error-handling-async | Async Operation Without Error Handling | scalability | HIGH | semgrep | javascript |
| js-pipeline-allocations | Multi-stage array pipeline allocates intermediate arrays | scalability | MEDIUM | semgrep | javascript |
| js-postmessage-no-origin | postMessage Listener Without Origin Validation | security | HIGH | semgrep | javascript |
| js-prf-json-deep-clone | Heavy Deep Clone via JSON Serialization | performance | MEDIUM | semgrep | javascript |
| js-prf-loop-invariant-case | Loop-Invariant Case Conversion in Iteration | performance | MEDIUM | semgrep | javascript |
| js-proto-pollution | Avoid prototype pollution via __proto__ | security | HIGH | semgrep | javascript |
| js-scl-await-in-loop | await Inside Loop (Sequential N+1 Data Fetching) | scalability | MEDIUM | semgrep | javascript |
| js-scl-foreach-async | Array.forEach() With Async Callback | scalability | MEDIUM | semgrep | javascript |
| js-sec-iframe-sandbox-bypass | Insecure iframe Sandbox Bypass | security | HIGH | semgrep | javascript |
| js-sec-iframe-srcdoc-xss | Unsandboxed Dynamic iframe srcDoc (Stored XSS) | security | HIGH | semgrep | javascript |
| js-unbounded-promise-all | Unbounded Promise.all over a dynamic array | scalability | HIGH | semgrep | javascript |
| js-unreachable-code | Unreachable code after return/throw/break/continue | maintainability | MEDIUM | semgrep | javascript |
| js-weak-crypto-hash | Weak hash on sensitive data (MD5/SHA1) | security | HIGH | semgrep | javascript |
| node-env-file-committed | Environment File With Secrets Committed to Repository | security | HIGH | regex | nodejs |
| node-excessive-dependencies | Excessive Number of Dependencies | scalability | LOW | regex | nodejs |
| node-no-api-keys-in-env-files | ENV check | security | HIGH | regex | nodejs |
| node-no-lint-config | No Linter Configuration | manageability | LOW | regex | nodejs |
| node-no-test-framework | No Test Framework Installed | manageability | MEDIUM | regex | nodejs |
| node-supabase-version-unpinned | Unpinned Supabase SDK Version | manageability | MEDIUM | regex | nodejs |
| node-wildcard-dependency | Wildcard Dependency Version | security | HIGH | regex | nodejs |
| php-arch-cognitive-overload-via-deep-block-nesting | Cognitive Overload via Deep Block Nesting | architecture | MEDIUM | semgrep | php |
| php-arch-concrete-class-empty-method-stub-refused-bequest-lsp-violation | Concrete Class Empty Method Stub (Refused Bequest & LSP Violation) | architecture | MEDIUM | semgrep | php |
| php-arch-encapsulation-breakdown-via-public-reference-returns-of-private-state | Encapsulation Breakdown via Public Reference Returns of Private State | architecture | HIGH | semgrep | php |
| php-arch-global-state-encapsulation-breach-via-global-keyword-inside-classes | Global State Encapsulation Breach via global Keyword inside Classes | architecture | HIGH | semgrep | php |
| php-arch-runtime-mutation-of-global-request-state-superglobal-request-pollution | Runtime Mutation of Global Request State (Superglobal Request Pollution) | architecture | HIGH | semgrep | php |
| php-mng-runtime-hardcoding-of-error-display-observability-logging-bypass | Runtime Hardcoding of Error Display (Observability & Logging Bypass) | manageability | HIGH | semgrep | php |
| php-mng-silent-exception-swallowing-empty-catch-blocks-destroying-observability | Silent Exception Swallowing (Empty catch Blocks Destroying Observability) | manageability | MEDIUM | semgrep | php |
| php-mng-unbounded-resource-allocation-overrides | Unbounded Resource Allocation Overrides | manageability | HIGH | semgrep | php |
| php-mng-unstructured-process-termination-die-exit-inside-functional-blocks | Unstructured Process Termination (die / exit) inside Functional Blocks | manageability | HIGH | semgrep | php |
| php-mnt-blind-observability-via-error-suppression-operator | Blind Observability via Error Suppression Operator (@) | maintainability | HIGH | semgrep | php |
| php-mnt-dangling-reference-pointers-leaking-from-foreach-loops | Dangling Reference Pointers Leaking from foreach Loops | maintainability | HIGH | semgrep | php |
| php-mnt-dynamic-variable-pollution-and-refactoring-sabotage-via-extract | Dynamic Variable Pollution and Refactoring Sabotage via extract() | maintainability | HIGH | semgrep | php |
| php-mnt-implicit-property-visibility-and-state-encapsulation-leakage | Implicit Property Visibility and State Encapsulation Leakage | maintainability | MEDIUM | semgrep | php |
| php-mnt-legacy-function-signature-contradiction | Legacy Function Signature Contradiction | maintainability | HIGH | semgrep | php |
| php-mnt-legacy-long-array-syntax-utilization | Legacy Long Array Syntax Utilization | maintainability | LOW | semgrep | php |
| php-mnt-loop-iterator-variable-shadowing-in-nested-structures | Loop Iterator Variable Shadowing in Nested Structures | maintainability | HIGH | semgrep | php |
| php-mnt-low-precedence-logical-operator-utilization-and-or-misuse | Low-Precedence Logical Operator Utilization (and / or Misuse) | maintainability | MEDIUM | semgrep | php |
| php-mnt-missing-curly-braces | Missing Curly Braces | maintainability | MEDIUM | semgrep | php |
| php-mnt-missing-default-fallback-case-in-switch-control-structures | Missing default Fallback Case in switch Control Structures | maintainability | MEDIUM | semgrep | php |
| php-mnt-missing-method-visibility-modifiers | Missing Method Visibility Modifiers | maintainability | MEDIUM | semgrep | php |
| php-mnt-readability-decay-via-nested-ternary-expressions | Readability Decay via Nested Ternary Expressions | maintainability | MEDIUM | semgrep | php |
| php-mnt-redundant-method-overriding-useless-parent-delegation | Redundant Method Overriding (Useless Parent Delegation) | maintainability | LOW | semgrep | php |
| php-mnt-redundant-trailing-return-statement-useless-end-of-block-return | Redundant Trailing Return Statement (Useless End-of-Block Return) | maintainability | LOW | semgrep | php |
| php-mnt-unreachable-dead-code-execution-paths-post-termination-statements | Unreachable Dead Code Execution Paths (Post-Termination Statements) | maintainability | MEDIUM | semgrep | php |
| php-prf-database-query-execution-inside-iterative-loops-procedural-n-plus-1-bottleneck | Database Query Execution Inside Iterative Loops (Procedural N+1 Bottleneck) | performance | HIGH | semgrep | php |
| php-prf-function-call-overhead-via-array-push-for-single-elements-inside-loops | Function Call Overhead via array_push for Single Elements Inside Loops | performance | MEDIUM | semgrep | php |
| php-prf-linear-array-scanning-via-in-array-inside-iterative-loops | Linear Array Scanning via in_array Inside Iterative Loops | performance | HIGH | semgrep | php |
| php-prf-loop-invariant-string-manipulation-code-hoisting-inefficiency | Loop-Invariant String Manipulation (Code Hoisting Inefficiency) | performance | MEDIUM | semgrep | php |
| php-prf-o-n-2-algorithmic-complexity-via-dynamic-count-evaluation-in-for-loop-conditions | $O(N^2)$ Algorithmic Complexity via Dynamic count() Evaluation in for Loop Conditions | performance | HIGH | semgrep | php |
| php-prf-quadratic-memory-allocation-via-array-merge-inside-loops | Quadratic Memory Allocation via array_merge Inside Loops | performance | HIGH | semgrep | php |
| php-prf-repetitive-file-descriptor-open-close-cycles-via-file-put-contents-inside-loops | Repetitive File Descriptor Open/Close Cycles via file_put_contents Inside Loops | performance | HIGH | semgrep | php |
| php-scl-catastrophic-memory-scaling-via-entire-file-slurping-for-iterative-processing | Catastrophic Memory Scaling via Entire File Slurping for Iterative Processing | scalability | HIGH | semgrep | php |
| php-scl-in-memory-array-accumulation-for-large-dataset-returns-missing-generators-yield | In-Memory Array Accumulation for Large Dataset Returns (Missing Generators/yield) | scalability | HIGH | semgrep | php |
| php-scl-memory-exhaustion-via-dynamic-range-array-generation-in-loop-iterators | Memory Exhaustion via Dynamic range() Array Generation in Loop Iterators | scalability | HIGH | semgrep | php |
| php-scl-memory-exhaustion-via-monolithic-result-set-loading-pdostatement-fetchall-in-loops | Memory Exhaustion via Monolithic Result Set Loading (PDOStatement::fetchAll) in Loops | scalability | HIGH | semgrep | php |
| php-scl-redundant-time-and-date-evaluation-inside-iterative-loops | Redundant Time and Date Evaluation Inside Iterative Loops | scalability | MEDIUM | semgrep | php |
| php-scl-synchronous-http-request-execution-inside-iterative-loops-api-n-plus-1-bottleneck | Synchronous HTTP Request Execution Inside Iterative Loops (API N+1 Bottleneck) | scalability | HIGH | semgrep | php |
| php-sec-cryptographic-hash-vulnerability-via-loose-comparison-type-juggling-magic-hashes | Cryptographic Hash Vulnerability via Loose Comparison (Type Juggling / Magic Hashes) | security | MEDIUM | semgrep | php |
| php-sec-direct-inline-sql-injection-via-http-superglobals-in-procedural-queries | Direct Inline SQL Injection via HTTP Superglobals in Procedural Queries | security | HIGH | semgrep | php |
| php-sec-disabled-ssl-tls-certificate-verification-in-curl-handles | Disabled SSL/TLS Certificate Verification in cURL Handles | security | HIGH | semgrep | php |
| php-sec-hardcoded-database-credentials-via-local-variable-assignment | Hardcoded Database Credentials via Local Variable Assignment | security | HIGH | semgrep | php |
| php-sec-insecure-cookie-attributes-missing-httponly-or-secure-flags | Insecure Cookie Attributes (Missing HttpOnly or Secure flags) | security | MEDIUM | semgrep | php |
| php-sec-insecure-cryptographic-cipher-mode-aes-ecb-in-native-openssl-functions | Insecure Cryptographic Cipher Mode (AES-ECB) in Native OpenSSL Functions | security | HIGH | semgrep | php |
| php-sec-overly-permissive-file-and-directory-permissions-0777 | Overly Permissive File and Directory Permissions (0777) | security | MEDIUM | semgrep | php |
| php-sec-production-information-disclosure-via-explicit-display-errors-activation | Production Information Disclosure via Explicit display_errors Activation | security | MEDIUM | semgrep | php |
| php-sec-sql-identifier-interpolation-and-structural-query-pollution | SQL Identifier Interpolation and Structural Query Pollution | security | MEDIUM | semgrep | php |
| php-sec-unsafe-native-deserialization-and-error-suppression | Unsafe Native Deserialization and Error Suppression | security | MEDIUM | semgrep | php |
| php-sec-unsafe-use-of-extract-with-untrusted-http-superglobals | Unsafe Use of extract() with Untrusted HTTP Superglobals | security | HIGH | semgrep | php |
| php-sec-use-of-cryptographically-broken-hash-functions-md5-sha1-on-sensitive-data | Use of Cryptographically Broken Hash Functions (md5 / sha1) on Sensitive Data | security | HIGH | semgrep | php |
| py-arch-assert-isinstance | assert isinstance(x, Y) | architecture | HIGH | semgrep | python |
| py-arch-dunder-import | __import__() direct call | architecture | LOW | semgrep | python |
| py-arch-global-keyword | global keyword used inside a function | architecture | LOW | semgrep | python |
| py-arch-reflection | globals()/locals()/vars() | architecture | MEDIUM | semgrep | python |
| py-arch-setattr-literal | setattr(obj, "literal", ...) | architecture | MEDIUM | semgrep | python |
| py-arch-type-eq | type(x) == X | architecture | HIGH | semgrep | python |
| py-arch-wildcard-import | from X import * | architecture | MEDIUM | semgrep | python |
| py-maint-broad-except | Broad except swallows errors | maintainability | HIGH | semgrep | python |
| py-maint-comparison-singleton | Comparison to None/True/False using == or != | maintainability | HIGH | semgrep | python |
| py-maint-else-after-return | Redundant else after return/raise | maintainability | HIGH | semgrep | python |
| py-maint-hardcoded-url-default | Hardcoded URL as os.getenv default | maintainability | MEDIUM | semgrep | python |
| py-maint-lambda-assignment | Lambda assigned to a variable | maintainability | LOW | semgrep | python |
| py-maint-legacy-typing | Legacy typing generics | maintainability | MEDIUM | semgrep | python |
| py-maint-logger-fstring | f-string inside logger call | maintainability | MEDIUM | semgrep | python |
| py-maint-mutable-default | Mutable default argument | maintainability | LOW | semgrep | python |
| py-maint-naive-datetime | Naive datetime | maintainability | MEDIUM | semgrep | python |
| py-maint-no-print | print() in production code | maintainability | MEDIUM | semgrep | python |
| py-mng-abs-path | Hardcoded absolute path | manageability | MEDIUM | semgrep | python |
| py-mng-assert-prod | assert for runtime validation | manageability | HIGH | semgrep | python |
| py-mng-bare-exception | raise Exception("...") | manageability | HIGH | semgrep | python |
| py-mng-ip-literal | IP/host literal hardcoded | manageability | MEDIUM | semgrep | python |
| py-mng-logging-basicconfig | logging.basicConfig outside __main__ | manageability | LOW | semgrep | python |
| py-mng-magic-timeout | Magic-number timeout | manageability | LOW | semgrep | python |
| py-mng-open-no-encoding | open() without explicit encoding | manageability | LOW | semgrep | python |
| py-mng-os-system | os.system(...) call | manageability | HIGH | semgrep | python |
| py-mng-subprocess-no-check | subprocess.run without check=True | manageability | MEDIUM | semgrep | python |
| py-mng-sys-exit-lib | sys.exit() outside __main__ | manageability | MEDIUM | semgrep | python |
| py-perf-async-requests | Synchronous requests.* in async function | performance | HIGH | semgrep | python |
| py-perf-async-sleep | time.sleep() in async function | performance | HIGH | semgrep | python |
| py-perf-dict-keys | Iterating dict.keys() instead of dict | maintainability | LOW | semgrep | python |
| py-perf-double-lookup | Double dict lookup | performance | LOW | semgrep | python |
| py-perf-len-zero | len(x) compared to 0 | performance | MEDIUM | semgrep | python |
| py-perf-list-in-agg | List comprehension inside aggregator | performance | MEDIUM | semgrep | python |
| py-perf-list-map-lambda | list(map/filter(lambda ...)) | performance | MEDIUM | semgrep | python |
| py-perf-open-no-with | open() not used in a with block | performance | HIGH | semgrep | python |
| py-perf-string-concat-loop | String concatenation with += in loop | performance | MEDIUM | semgrep | python |
| py-scal-deepcopy | copy.deepcopy(...) flag | performance | MEDIUM | semgrep | python |
| py-scal-lru-on-self | @lru_cache on instance method | scalability | HIGH | semgrep | python |
| py-scal-mutable-class-attr | Mutable class-level attribute | scalability | HIGH | semgrep | python |
| py-scal-range-len | for i in range(len(x)) | scalability | LOW | semgrep | python |
| py-scal-requests-no-timeout | requests without timeout= | scalability | MEDIUM | semgrep | python |
| py-scal-subprocess-no-timeout | subprocess without timeout= | scalability | HIGH | semgrep | python |
| py-scal-thread-fire-forget | Thread fire-and-forget | scalability | MEDIUM | semgrep | python |
| py-sec-eval-exec | eval/exec/compile | security | HIGH | semgrep | python |
| py-sec-hardcoded-secret | Hardcoded secret literal | security | MEDIUM | semgrep | python |
| py-sec-mktemp | tempfile.mktemp() race | security | MEDIUM | semgrep | python |
| py-sec-pickle-load | pickle/marshal deserialization | security | HIGH | semgrep | python |
| py-sec-random-secret | random.* for tokens/secrets | security | MEDIUM | semgrep | python |
| py-sec-shell-true | subprocess with shell=True | security | HIGH | semgrep | python |
| py-sec-tls-verify-false | verify=False in requests/httpx | security | HIGH | semgrep | python |
| py-sec-weak-hash | hashlib.md5/sha1 | security | HIGH | semgrep | python |
| py-sec-xml-xxe | Stdlib XML (XXE risk) | security | HIGH | semgrep | python |
| py-sec-yaml-load | yaml.load without SafeLoader | security | HIGH | semgrep | python |
| rct-dangerous-inner-html | dangerouslySetInnerHTML Used Without Sanitisation | security | HIGH | semgrep | react |
| rct-literal-effect-deps | Literal object/array in hook dependency array | performance | HIGH | semgrep | react |
| rct-mixed-concerns | Mixed Data Fetching and Rendering Concerns | manageability | MEDIUM | semgrep | react |
| rct-mnt-conditional-hook | React Hook Called Conditionally (Syntactic Isolation) | maintainability | HIGH | semgrep | react |
| rct-no-error-boundary | Missing React Error Boundary | scalability | MEDIUM | semgrep | react |
| rct-no-loading-state | Data Fetching Without Loading State | manageability | MEDIUM | semgrep | react |
| rct-open-redirect | Potential Open Redirect via Dynamic Navigation | security | MEDIUM | semgrep | react |
| rct-prf-jsonstringify-deps | JSON.stringify inside Hook Dependency Array | performance | MEDIUM | semgrep | react |
| rct-prf-setstate-in-useeffect | Synchronous setState Inside useEffect | performance | HIGH | semgrep | react |
| rct-unsafe-href-binding | Dynamic Value Bound to href Without URL Validation | security | HIGH | semgrep | react |
| rct-unvalidated-url-params | Unvalidated URL Search Params Rendered in JSX | security | MEDIUM | semgrep | react |
| rct-useeffect-missing-cleanup | useEffect With Subscription But No Cleanup | performance | MEDIUM | semgrep | react |
| rct-useeffect-no-deps | useEffect Without Dependency Array | performance | HIGH | semgrep | react |
| adobe-action-flag-usage-avoid | ActionFlag Usage Should Be Avoided | manageability | HIGH | regex | regex-tool-adobe-magento |
| adobe-auth-controller-avoid | Authentication In Controller Should Be Avoided | security | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-business-logic-in-phtml | Business Logic In PHTML Templates Should Be Avoided | architecture | HIGH | regex | regex-tool-adobe-magento |
| adobe-deprecated-controller | Deprecated Controller Inheritance Should Be Avoided | manageability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-direct-db-calls-plugins | Direct Database Calls In Plugins Should Be Avoided | scalability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-direct-exit-avoid | Direct Exit Should Be Avoided | scalability | HIGH | regex | regex-tool-adobe-magento |
| adobe-direct-html-output | Direct HTML Output Should Be Avoided | performance | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-direct-model-extension | Direct Model Extension Should Be Avoided | scalability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-direct-object-manager | Direct ObjectManager Usage Should Be Avoided | scalability | HIGH | regex | regex-tool-adobe-magento |
| adobe-direct-plugin-modify | Direct Modification In Plugins Should Be Avoided | performance | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-direct-result-modify | Direct Result Modification Should Be Avoided | performance | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-direct-sql-query-build | Direct SQL Query Construction Should Be Avoided | security | HIGH | regex | regex-tool-adobe-magento |
| adobe-direct-template-assign | Direct Template Assignment Should Be Avoided | manageability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-directory-write-avoid | Directory Write Check Should Be Avoided | security | HIGH | regex | regex-tool-adobe-magento |
| adobe-empty-catch-block | Empty Catch Block Should Be Avoided | security | HIGH | regex | regex-tool-adobe-magento |
| adobe-exception-handling-no-log | Exception Handling Without Logging Should Be Avoided | manageability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-extend-sales-collections | Extending Sales Collections Should Be Avoided | scalability | HIGH | regex | regex-tool-adobe-magento |
| adobe-extension-attribute-check | Extension Attribute Existence Should Be Verified | manageability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-false-return-after-plugin | Returning False In After Plugin Should Be Avoided | scalability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-generic-exception-avoid | Catching Generic Exception Should Be Avoided | manageability | HIGH | regex | regex-tool-adobe-magento |
| adobe-hardcoded-urls-avoid | Hardcoded URLs Should Be Avoided | scalability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-html-attribute-concat | HTML Attribute Concatenation Should Be Avoided | performance | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-leading-backslashes-use | Leading Backslashes In Use Statements Should Be Avoided | manageability | LOW | regex | regex-tool-adobe-magento |
| adobe-magento-class-override | Core Magento Class Override Should Be Avoided | maintainability | HIGH | regex | regex-tool-adobe-magento |
| adobe-missing-phpdoc-block | Missing PHPDoc Block Should Be Avoided | manageability | LOW | regex | regex-tool-adobe-magento |
| adobe-null-check-block-create | Null Check in Block Creation Should Be Avoided | performance | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-output-buffering-avoid | Output Buffering Should Be Avoided | performance | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-package-annotation-avoid | Package Annotation Should Be Avoided | manageability | LOW | regex | regex-tool-adobe-magento |
| adobe-parameter-type-hint-avoid | Parameter Type Hint Should Be Avoided | scalability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-private-methods-plugins | Private Methods In Plugins Should Be Avoided | manageability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-registry-manipulation | Direct Registry Manipulation Should Be Avoided | manageability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-return-type-spec-avoid | Return Type Specification Should Be Avoided | scalability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-string-resource-model | Direct String Resource Model Should Be Avoided | manageability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-undefined-parent-classes | Undefined Parent Classes Should Be Avoided | manageability | HIGH | regex | regex-tool-adobe-magento |
| adobe-untranslated-user-text | User-Visible Text Should Be Translated | manageability | MEDIUM | regex | regex-tool-adobe-magento |
| adobe-use-repository-pattern | Repository Pattern Should Be Used | architecture | MEDIUM | regex | regex-tool-adobe-magento |
| sa-arch-legacy-column-style | Legacy Column() without Mapped[] | architecture | MEDIUM | semgrep | sqlalchemy |
| sa-arch-mapper-in-init | Mapping logic in __init__ | architecture | MEDIUM | semgrep | sqlalchemy |
| sa-arch-mixed-orm-core | Mixing query() and select() in same module | architecture | LOW | semgrep | sqlalchemy |
| sa-arch-query-api-deprecated | 1.x Query API used | architecture | MEDIUM | semgrep | sqlalchemy |
| sa-arch-relationship-class-ref | relationship(ConcreteClass) | architecture | LOW | semgrep | sqlalchemy |
| sa-mng-backref-not-back-populates | relationship using backref= | manageability | LOW | semgrep | sqlalchemy |
| sa-mng-create-all-in-prod | Base.metadata.create_all in app code | manageability | HIGH | semgrep | sqlalchemy |
| sa-mng-fk-no-index | ForeignKey column without index=True | performance | HIGH | semgrep | sqlalchemy |
| sa-mng-hardcoded-engine-url | create_engine with literal URL | manageability | HIGH | semgrep | sqlalchemy |
| sa-mng-no-cascade | relationship without cascade= | manageability | MEDIUM | semgrep | sqlalchemy |
| sa-mng-no-naming-convention | MetaData without naming_convention | manageability | MEDIUM | semgrep | sqlalchemy |
| sa-mng-no-onupdate-timestamp | updated_at without onupdate | manageability | MEDIUM | semgrep | sqlalchemy |
| sa-mng-no-server-default-timestamp | created_at without server_default | manageability | MEDIUM | semgrep | sqlalchemy |
| sa-mng-server-default-and-onupdate | server_default + Python onupdate mismatch | manageability | MEDIUM | semgrep | sqlalchemy |
| sa-mnt-fk-no-ondelete | ForeignKey without ondelete= | maintainability | MEDIUM | semgrep | sqlalchemy |
| sa-mnt-no-passive-deletes | Cascade delete-orphan without passive_deletes | maintainability | MEDIUM | semgrep | sqlalchemy |
| sa-mnt-no-tablename | Model without __tablename__ | maintainability | LOW | semgrep | sqlalchemy |
| sa-mnt-relationship-no-type | relationship without type hint | maintainability | LOW | semgrep | sqlalchemy |
| sa-prf-commit-in-loop | session.commit() inside loop | performance | HIGH | semgrep | sqlalchemy |
| sa-prf-count-via-all | len() over query.all() | performance | HIGH | semgrep | sqlalchemy |
| sa-prf-execute-text-raw | execute() with raw SQL string | performance | MEDIUM | semgrep | sqlalchemy |
| sa-prf-flush-in-loop | session.flush() inside loop | performance | MEDIUM | semgrep | sqlalchemy |
| sa-prf-load-all-columns | Selecting full model when one column needed | performance | MEDIUM | semgrep | sqlalchemy |
| sa-prf-n-plus-one | N+1 lazy loading in loop | performance | HIGH | semgrep | sqlalchemy |
| sa-prf-no-bulk-insert | Loop of session.add() instead of bulk insert | performance | MEDIUM | semgrep | sqlalchemy |
| sa-prf-no-eager-load | Query without eager loading | performance | HIGH | semgrep | sqlalchemy |
| sa-prf-relationship-no-lazy | relationship() without explicit lazy= | performance | LOW | semgrep | sqlalchemy |
| sa-scl-autoflush-loop | autoflush=True with relationship mutation in loop | scalability | MEDIUM | semgrep | sqlalchemy |
| sa-scl-create-engine-in-function | create_engine() called inside a function | scalability | HIGH | semgrep | sqlalchemy |
| sa-scl-global-session | Module-level Session() instance | scalability | HIGH | semgrep | sqlalchemy |
| sa-scl-no-isolation-level | create_engine without isolation_level | scalability | LOW | semgrep | sqlalchemy |
| sa-scl-no-pool-pre-ping | create_engine without pool_pre_ping | scalability | MEDIUM | semgrep | sqlalchemy |
| sa-scl-no-pool-recycle | create_engine without pool_recycle | scalability | HIGH | semgrep | sqlalchemy |
| sa-scl-no-session-close | Session without context manager | scalability | HIGH | semgrep | sqlalchemy |
| sa-scl-sync-in-async | Sync Session inside async function | scalability | HIGH | semgrep | sqlalchemy |
| sa-sec-engine-echo-prod | create_engine(echo=True) | security | HIGH | semgrep | sqlalchemy |
| sa-sec-engine-url-secret | Engine URL with literal password | security | HIGH | semgrep | sqlalchemy |
| sa-sec-execute-concat | execute() with string concat | security | HIGH | semgrep | sqlalchemy |
| sa-sec-execute-percent | execute() with % formatting | security | HIGH | semgrep | sqlalchemy |
| sa-sec-filter-string | filter() with raw string | security | HIGH | semgrep | sqlalchemy |
| sa-sec-no-ssl-postgres | Postgres URL without sslmode | security | HIGH | semgrep | sqlalchemy |
| sa-sec-pickle-type | PickleType column | security | HIGH | semgrep | sqlalchemy |
| sa-sec-text-fstring | text() with f-string | security | HIGH | semgrep | sqlalchemy |
| sa-sec-text-no-bindparams | text() with :param but no binding | security | MEDIUM | semgrep | sqlalchemy |
| sb-auth-localstorage-token | Manual Token Storage in localStorage | security | HIGH | semgrep | supabase |
| sb-auth-no-session-check | Protected Route Without Session Check | security | HIGH | regex | supabase |
| sb-auth-reversed-logic | Reversed Auth Guard Logic | security | HIGH | semgrep | supabase |
| sb-exposed-service-role-key | Exposed Supabase Service Role Key | security | HIGH | semgrep | supabase |
| sb-hardcoded-anon-key | Hardcoded Supabase Anon Key | security | MEDIUM | semgrep | supabase |
| sb-hardcoded-supabase-url | Hardcoded Supabase Project URL | security | HIGH | semgrep | supabase |
| sb-jwt-client-decode | Client-Side JWT Decoding | security | HIGH | regex | supabase |
| sb-mutation-no-error | Supabase Mutation Without Error Handling | security | HIGH | semgrep | supabase |
| sb-no-rate-limiting | No Rate Limiting on Edge Functions | scalability | HIGH | semgrep | supabase |
| sb-single-supabase-project | Single Supabase Project Used Across All Environments | manageability | MEDIUM | semgrep | supabase |
| sb-storage-public-bucket | Public Supabase Storage Bucket Reference | security | MEDIUM | semgrep | supabase |
| sb-supabase-admin-client | Supabase Admin Client in Frontend Code | security | HIGH | semgrep | supabase |
| ts-ai-provider-key | AI Provider API Key in Source Code | security | HIGH | regex | typescript |
| ts-any-type-usage | TypeScript any Type Usage | manageability | MEDIUM | semgrep | typescript |
| ts-api-key-in-client | Third-Party API Key Exposed in Client Code | security | HIGH | semgrep | typescript |
| ts-aws-credentials | AWS Credentials in Source Code | security | HIGH | semgrep | typescript |
| ts-db-connection-string | Database Connection String With Credentials | security | HIGH | semgrep | typescript |
| ts-firebase-config-exposed | Firebase Configuration Object in Source Code | security | MEDIUM | semgrep | typescript |
| ts-generic-secret-assignment | Hardcoded Secret Assignment in Source Code | security | HIGH | regex | typescript |
| ts-git-platform-token | Git Platform Access Token in Source Code | security | HIGH | regex | typescript |
| ts-hardcoded-bearer-token | Hardcoded Bearer Token in HTTP Headers | security | HIGH | semgrep | typescript |
| ts-messaging-service-key | Messaging Service Credentials in Source Code | security | HIGH | regex | typescript |
| ts-missing-strict | TypeScript Strict Mode Not Enabled | manageability | MEDIUM | regex | typescript |
| ts-private-key-in-code | Private Key Material in Source Code | security | HIGH | semgrep | typescript |
| vite-env-no-vite-prefix | Non-VITE_ Environment Variable in Client Code | security | MEDIUM | semgrep | vite |
| vite-hardcoded-config | Hardcoded Configuration Values | manageability | MEDIUM | semgrep | vite |
| vite-missing-csp | Missing Content Security Policy | security | HIGH | regex | vite |
| vite-missing-referrer-policy | Missing Referrer-Policy Header | security | MEDIUM | semgrep | vite |
| vite-missing-sri | CDN Script Tag Without Subresource Integrity | security | MEDIUM | semgrep | vite |
| vite-production-url-in-code | Production Supabase URL in Source Code | security | HIGH | semgrep | vite |
