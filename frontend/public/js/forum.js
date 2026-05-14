// Pyodide is loaded globally from CDN in HTML via:
// <script src="https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"></script>

let pyodideReadyPromise = null;

function getPyodideReady() {
    if (!pyodideReadyPromise) {
        pyodideReadyPromise = loadPyodide({
            indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/"
        });
    }
    return pyodideReadyPromise;
}

// Toggle the visibility of the new topic form
function toggleForm() {
    const form = document.getElementById('new-topic-form');
    if (form) {
        const current = form.style.display;
        form.style.display = (current === 'none' || current === '') ? 'block' : 'none';
    }
}

// Make toggleForm available for inline onclick handlers
window.toggleForm = toggleForm;

function attachPythonCodeValidation(form) {
    if (!form) return;

    form.addEventListener('submit', async function (event) {
        event.preventDefault(); // stop native submit until validation finishes

        const codeField = form.querySelector('#topic-code');
        if (!codeField) {
            form.submit();
            return;
        }

        const value = codeField.value.trim();

        // Required field
        if (!value) {
            alert('Пожалуйста, введите пример Python-кода.');
            codeField.focus();
            return;
        }

        // Block HTML tags
        if (/<[^>]+>/.test(value)) {
            alert('Код не должен содержать HTML-теги. Оставьте только Python-код.');
            codeField.focus();
            return;
        }

        try {
            const pyodide = await getPyodideReady();

            // Pass code safely into Python runtime
            pyodide.globals.set("code_to_check", value);

            // Strict Python validation
            pyodide.runPython(`
                import ast
                
                tree = ast.parse(code_to_check)
                
                if not tree.body:
                    raise ValueError("Введите настоящий Python-код.")
                
                # If only one statement and it's an expression → allow ONLY function calls
                if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):
                    expr = tree.body[0].value
                
                    # Allow function calls: print(...), foo(), bar(1)
                    if not isinstance(expr, ast.Call):
                        raise ValueError("Введите настоящий Python-код, а не произвольный текст.")
                `);

            // All good — submit
            form.submit();

        } catch (err) {
            alert("Ошибка Python-кода:\n" + err);
            codeField.focus();
        }
    });
}

// Initialize forms when the page loads
document.addEventListener('DOMContentLoaded', function () {
    const inlineFormContainer = document.getElementById('new-topic-form');
    if (inlineFormContainer) {
        inlineFormContainer.style.display = 'none';
        const inlineForm = inlineFormContainer.querySelector('form');
        attachPythonCodeValidation(inlineForm);
    }

    const altForm = document.querySelector('.forum-container .topic-form form');
    if (altForm && (!inlineFormContainer || !inlineFormContainer.contains(altForm))) {
        attachPythonCodeValidation(altForm);
    }
});