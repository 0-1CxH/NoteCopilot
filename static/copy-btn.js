// (1) Copy button on hover for code blocks, tables, details/summary
function addCopyButtons() {
    // Helper to create the button
    function createCopyBtn() {
        const btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.innerHTML = 'COPY';
        btn.style.position = 'absolute';
        btn.style.top = '8px';
        btn.style.left = '8px';
        btn.style.zIndex = '10000';
        btn.style.display = 'block'; // Make it visible by default for debugging
        btn.style.padding = '4px 10px';
        btn.style.fontSize = '0.95em';
        btn.style.background = 'rgba(59, 130, 246, 0.9)'; // More opaque for visibility
        btn.style.color = '#fff';
        btn.style.border = '2px solid #fff'; // Add border for visibility
        btn.style.borderRadius = '6px';
        btn.style.cursor = 'pointer';
        btn.style.boxShadow = '0 2px 8px 0 rgba(99,102,241,0.3)';
        btn.style.transition = 'background 0.2s';
        btn.addEventListener('mouseenter', () => btn.style.background = 'rgba(37, 99, 235, 0.8)'); // blue-600 with transparency
        btn.addEventListener('mouseleave', () => btn.style.background = 'rgba(59, 130, 246, 0.6)'); // blue-500 with transparency
        return btn;
    }

    // For code blocks (table.highlighttable), tables (table.markdown-table), details/summary, and AI message components
    const selectors = [
        'table.highlighttable',
        'table.markdown-table',
        'table',
        'details',
        'ai-message-component-think',
        'ai-message-component-response'
    ];
    
    let totalElements = 0;
    let aiElements = 0;
    
    selectors.forEach(sel => {
        const elements = document.querySelectorAll(sel);
        console.log(`Selector "${sel}" found ${elements.length} elements`);
        
        elements.forEach(block => {
            totalElements++;
            if (sel === 'ai-message-component-think' || sel === 'ai-message-component-response') {
                aiElements++;
                console.log(`Processing AI element:`, block);
                console.log('AI element position:', block.style.position);
                console.log('AI element z-index:', block.style.zIndex);
            }
            
            // Make sure the block is relatively positioned
            block.style.position = 'relative';
            // Add transition for smooth box-shadow animation
            block.style.transition = 'box-shadow 0.3s ease';
            // Only add one button per block
            // if (block.querySelector('.copy-btn')) {
            //     console.log('Copy button already exists, skipping');
            //     return;
            // }
            const btn = createCopyBtn();
            block.appendChild(btn);
            console.log(`Added copy button to ${sel} element`);
            console.log('Button position:', btn.style.position);
            console.log('Button z-index:', btn.style.zIndex);
            console.log('Button display:', btn.style.display);
            
            // For AI elements, keep button visible for debugging
            if (sel === 'ai-message-component-think' || sel === 'ai-message-component-response') {
                btn.style.display = 'block';
            } else {
                btn.style.display = 'none';
            }
            
            block.addEventListener('mouseenter', () => {
                if (sel !== 'ai-message-component-think' && sel !== 'ai-message-component-response') {
                    btn.style.display = 'block';
                }
                // Add blur effect to box-shadow
                block.style.boxShadow = '0 0 20px rgba(59, 130, 246, 0.3)';
            });
            block.addEventListener('mouseleave', () => {
                if (sel !== 'ai-message-component-think' && sel !== 'ai-message-component-response') {
                    btn.style.display = 'none';
                }
                // Remove blur effect
                block.style.boxShadow = '';
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
                } else if (block.matches('table')) {
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
                } else if (block.matches('ai-message-component-think') || block.matches('ai-message-component-response')) {
                    // Get original markdown content from data attribute
                    text = block.getAttribute('data-original-content') || block.innerText;
                    console.log('Copying AI component text:', text.substring(0, 100) + '...');
                }
                navigator.clipboard.writeText(text);
                btn.innerHTML = 'COPIED!';
                setTimeout(() => { btn.innerHTML = 'COPY'; }, 1200);
            });
        });
    });
    
    console.log(`Total elements processed: ${totalElements}, AI elements: ${aiElements}`);
}

// Function to retry adding copy buttons for dynamic content
// function retryAddCopyButtons() {
    // setTimeout(() => {
    //     console.log('Retrying to add copy buttons for dynamic content...');
    //     addCopyButtons();
    // }, 1000);
// }


document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - adding copy buttons');
    addCopyButtons();
    // addQueryButton();
    
    // Also retry after a delay to catch any dynamically loaded content
    // retryAddCopyButtons();
});

// Also listen for any dynamic content changes
document.addEventListener('DOMNodeInserted', (event) => {
    if (event.target.matches && (event.target.matches('ai-message-component-think') || event.target.matches('ai-message-component-response'))) {
        console.log('New AI component detected, retrying copy buttons');
        // retryAddCopyButtons();
    }
});
