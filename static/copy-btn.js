// (1) Copy button on hover for code blocks, tables, details/summary
function addCopyButtons() {
    // Helper to create the button
    function createCopyBtn() {
        const btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.innerHTML = 'COPY';
        btn.style.position = 'absolute';
        btn.style.top = '8px';
        btn.style.right = '8px';
        btn.style.zIndex = '10';
        btn.style.display = 'none';
        btn.style.padding = '4px 10px';
        btn.style.fontSize = '0.95em';
        btn.style.background = '#3b82f6';
        btn.style.color = '#fff';
        btn.style.border = 'none';
        btn.style.borderRadius = '6px';
        btn.style.cursor = 'pointer';
        btn.style.boxShadow = '0 2px 8px 0 rgba(99,102,241,0.13)';
        btn.style.transition = 'background 0.2s';
        btn.addEventListener('mouseenter', () => btn.style.background = '#2563eb'); // blue-600
        btn.addEventListener('mouseleave', () => btn.style.background = '#3b82f6'); // blue-500
        return btn;
    }

    // For code blocks (table.highlighttable), tables (table.markdown-table), details/summary
    const selectors = [
        'table.highlighttable',
        'table.markdown-table',
        'details'
    ];
    selectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(block => {
            // Make sure the block is relatively positioned
            block.style.position = 'relative';
            // Only add one button per block
            if (block.querySelector('.copy-btn')) return;
            const btn = createCopyBtn();
            block.appendChild(btn);
            block.addEventListener('mouseenter', () => {
                btn.style.display = 'block';
            });
            block.addEventListener('mouseleave', () => {
                btn.style.display = 'none';
            });
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                let text = '';
                if (block.matches('table.highlighttable')) {
                    // Get code text from code block
                    const code = block.querySelector('td.code pre');
                    text = code ? code.innerText : block.innerText;
                } else if (block.matches('table.markdown-table')) {
                    // Clone the table and remove all .copy-btn before copying
                    let temp = block.cloneNode(true);
                    temp.querySelectorAll('.copy-btn').forEach(btn => btn.remove());
                    text = temp.innerText;
                } else if (block.matches('details')) {
                    // Exclude summary and copy button itself
                    let temp = block.cloneNode(true);
                    // Remove all .copy-btn
                    temp.querySelectorAll('.copy-btn').forEach(btn => btn.remove());
                    // Remove all summary tags
                    temp.querySelectorAll('summary').forEach(s => s.remove());
                    text = temp.innerText;
                }
                navigator.clipboard.writeText(text);
                btn.innerHTML = 'COPIED!';
                setTimeout(() => { btn.innerHTML = 'COPY'; }, 1200);
            });
        });
    });
}

// // (2) Query button on text selection
// function addQueryButton() {
//     let queryBtn = null;
//     let lastRange = null;
//     let lastSelectedText = '';
//     function createQueryBtn() {
//         const btn = document.createElement('button');
//         btn.className = 'query-btn';
//         btn.innerHTML = 'ASK';
//         btn.style.position = 'fixed';
//         btn.style.zIndex = '9999';
//         btn.style.display = 'none';
//         btn.style.padding = '4px 12px';
//         btn.style.fontSize = '1em';
//         btn.style.background = '#2563eb';
//         btn.style.color = '#fff';
//         btn.style.border = 'none';
//         btn.style.borderRadius = '6px';
//         btn.style.cursor = 'pointer';
//         btn.style.boxShadow = '0 2px 8px 0 rgba(37,99,235,0.13)';
//         btn.style.transition = 'background 0.2s';
//         btn.addEventListener('mouseenter', () => btn.style.background = '#1d4ed8');
//         btn.addEventListener('mouseleave', () => btn.style.background = '#2563eb');
//         btn.addEventListener('mousedown', e => e.preventDefault());
//         return btn;
//     }
//     function showQueryBtn(x, y) {
//         if (!queryBtn) {
//             queryBtn = createQueryBtn();
//             document.body.appendChild(queryBtn);
//             queryBtn.addEventListener('click', () => {
//                 if (!lastRange) return;
//                 queryBtn.style.display = 'none'; // Hide immediately on click
//                 const sel = window.getSelection();
//                 sel.removeAllRanges();
//                 sel.addRange(lastRange);
//                 const text = sel.toString();
//                 fetch('http://localhost:8000/query', {
//                     method: 'POST',
//                     headers: { 'Content-Type': 'application/json' },
//                     body: JSON.stringify({ query: text })
//                 }).then(() => {
//                     queryBtn.innerHTML = '!';
//                     setTimeout(() => { queryBtn.innerHTML = 'ASK'; }, 1200);
//                 });
//             });
//         }
//         queryBtn.style.left = `${x}px`;
//         queryBtn.style.top = `${y}px`;
//         queryBtn.style.display = 'block';
//     }
//     document.addEventListener('mouseup', (e) => {
//         setTimeout(() => {
//             const sel = window.getSelection();
//             if (sel && sel.toString().trim().length > 0) {
//                 const selectedText = sel.toString();
//                 if (selectedText === lastSelectedText) {
//                     // Do not show button if selection is the same as last time
//                     return;
//                 }
//                 lastRange = sel.getRangeAt(0).cloneRange();
//                 lastSelectedText = selectedText;
//                 // Show button near mouse
//                 showQueryBtn(e.clientX + 10, e.clientY + 10);
//             } else if (queryBtn) {
//                 queryBtn.style.display = 'none';
//                 lastSelectedText = '';
//             }
//         }, 10);
//     });
//     document.addEventListener('mousedown', (e) => {
//         if (queryBtn && !queryBtn.contains(e.target)) {
//             queryBtn.style.display = 'none';
//         }
//     });
// }

document.addEventListener('DOMContentLoaded', () => {
    addCopyButtons();
    // addQueryButton();
});
