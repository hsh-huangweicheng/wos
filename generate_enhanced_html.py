import base64

# Read the base64 config
with open('config_base64.txt', 'r', encoding='utf-8') as f:
    config_base64 = f.read().strip()

html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WOS记录解析工具 - 增强版</title>
    <script src="https://cdn.sheetjs.com/xlsx-0.20.0/package/dist/xlsx.full.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 20px; font-size: 1.8rem; text-shadow: 0 2px 4px rgba(0,0,0,0.2); }
        h1 .help-btn { font-size: 0.7rem; background: rgba(255,255,255,0.2); border: none; color: white; padding: 4px 10px; border-radius: 15px; cursor: pointer; margin-left: 10px; vertical-align: middle; }
        h1 .help-btn:hover { background: rgba(255,255,255,0.3); }
        .card { background: white; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); padding: 25px; margin-bottom: 20px; }
        .card-title { font-size: 1.1rem; color: #333; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #667eea; display: flex; justify-content: space-between; align-items: center; }
        .card-title .title-text { font-weight: 600; }
        .card-title .controls { display: flex; gap: 10px; align-items: center; }
        .upload-area {
            border: 3px dashed #667eea; border-radius: 12px; padding: 35px 20px;
            text-align: center; cursor: pointer; transition: all 0.3s ease; background: #f8f9ff;
        }
        .upload-area:hover { border-color: #764ba2; background: #f0f2ff; }
        .upload-area.dragover { border-color: #764ba2; background: #e8ebff; transform: scale(1.02); }
        .upload-area.small { padding: 25px 20px; }
        .upload-icon { font-size: 40px; margin-bottom: 12px; }
        .upload-text { color: #555; font-size: 0.95rem; }
        .upload-hint { color: #888; font-size: 0.8rem; margin-top: 8px; }
        #fileInput, #configInput { display: none; }
        .file-list { margin-top: 12px; }
        .file-item { display: flex; align-items: center; justify-content: space-between; padding: 8px 12px; background: #f8f9fa; border-radius: 8px; margin-bottom: 6px; }
        .file-name { color: #333; font-weight: 500; font-size: 0.9rem; }
        .file-remove { color: #dc3545; cursor: pointer; font-size: 1.1rem; padding: 0 8px; }
        .btn { display: inline-block; padding: 10px 20px; border: none; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; margin: 4px; }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); }
        .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
        .btn-success { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; }
        .btn-success:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(40, 167, 69, 0.4); }
        .btn-secondary { background: #6c757d; color: white; }
        .btn-secondary:hover { background: #5a6268; }
        .btn-group { text-align: center; margin-top: 12px; }
        .config-status { padding: 10px 12px; border-radius: 8px; margin-top: 12px; font-size: 0.85rem; }
        .config-status.loaded { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .config-status.default { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 8px; margin: 12px 0; }
        .stat-item { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px; border-radius: 8px; text-align: center; }
        .stat-number { font-size: 1.2rem; font-weight: bold; }
        .stat-label { font-size: 0.7rem; opacity: 0.9; margin-top: 3px; }
        .preview-container { margin-top: 12px; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; }
        .preview-toolbar { display: flex; justify-content: space-between; align-items: center; padding: 10px 15px; background: #f8f9fa; border-bottom: 1px solid #e0e0e0; flex-wrap: wrap; gap: 10px; }
        .preview-toolbar .page-info { font-size: 0.85rem; color: #666; }
        .preview-toolbar select { padding: 5px 10px; border-radius: 4px; border: 1px solid #ddd; }
        .preview-toolbar button { padding: 5px 12px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
        .preview-toolbar button:disabled { opacity: 0.5; cursor: not-allowed; }
        .preview-table-wrapper { }
        .preview-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
        .preview-table th { background: #667eea; color: white; padding: 8px 6px; text-align: left; position: sticky; top: 0; white-space: nowrap; }
        .preview-table th input { width: 100%; padding: 3px 5px; border: 1px solid #ddd; border-radius: 3px; margin-top: 4px; font-size: 0.75rem; }
        .preview-table td { padding: 6px; border-bottom: 1px solid #e0e0e0; max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .preview-table tr:hover { background: #f8f9ff; }
        .preview-table td.highlight { background: #ffcccc !important; }
        .alert { padding: 10px 12px; border-radius: 8px; margin: 12px 0; font-size: 0.85rem; }
        .alert-info { background: #e7f3ff; color: #0056b3; border: 1px solid #b3d7ff; }
        .loading { display: none; text-align: center; padding: 20px; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; width: 36px; height: 36px; animation: spin 1s linear infinite; margin: 0 auto 12px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .hidden { display: none !important; }
        .two-column { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        @media (max-width: 768px) { .two-column { grid-template-columns: 1fr; } }
        /* Modal styles */
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; }
        .modal.show { display: flex; justify-content: center; align-items: center; }
        .modal-content { background: white; border-radius: 12px; padding: 30px; max-width: 700px; max-height: 80vh; overflow-y: auto; margin: 20px; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .modal-header h2 { color: #333; font-size: 1.3rem; }
        .modal-close { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #666; }
        .modal-body { line-height: 1.8; color: #444; }
        .modal-body h3 { color: #667eea; margin: 20px 0 10px; font-size: 1.1rem; }
        .modal-body ul { margin-left: 20px; }
        .modal-body code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: monospace; }
        .modal-body .example { background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>WOS记录解析工具 - 增强版 <button class="help-btn" id="helpBtn">帮助</button></h1>
        <div class="two-column">
            <div class="card">
                <div class="card-title"><span class="title-text">WOS文件上传</span></div>
                <div class="upload-area" id="uploadArea">
                    <div class="upload-icon">📄</div>
                    <div class="upload-text">点击或拖拽上传WOS导出的TXT文件</div>
                    <div class="upload-hint">支持同时上传多个文件</div>
                    <input type="file" id="fileInput" multiple accept=".txt">
                </div>
                <div class="file-list" id="fileList"></div>
                <div class="btn-group">
                    <button class="btn btn-primary" id="parseBtn" disabled>解析文件</button>
                    <button class="btn btn-secondary" id="clearBtn" disabled>清空</button>
                </div>
            </div>
            <div class="card">
                <div class="card-title"><span class="title-text">配置管理</span></div>
                <div class="upload-area small" id="configArea">
                    <div class="upload-text">点击上传自定义配置（Excel）</div>
                    <div class="upload-hint">不上传则使用内置默认配置</div>
                    <input type="file" id="configInput" accept=".xlsx,.xls">
                </div>
                <div class="config-status default" id="configStatus">使用内置默认配置</div>
                <div class="btn-group">
                    <button class="btn btn-secondary" id="downloadConfigBtn">下载示例配置</button>
                    <button class="btn btn-secondary" id="resetConfigBtn">重置</button>
                </div>
            </div>
        </div>
        <div class="card hidden" id="resultCard">
            <div class="card-title">
                <span class="title-text">解析结果</span>
            </div>
            <div class="stats" id="stats"></div>
            <div class="alert alert-info" id="resultInfo"></div>
            <div class="btn-group">
                <button class="btn btn-success" id="downloadBtn">下载Excel文件</button>
            </div>
            <div class="preview-container" id="previewContainer">
                <div class="preview-toolbar">
                    <div class="page-info">
                        <span id="pageInfoText">第 1-25 条，共 0 条</span>
                    </div>
                    <div>
                        <label>每页显示: </label>
                        <select id="pageSize">
                            <option value="25">25条</option>
                            <option value="50">50条</option>
                            <option value="100">100条</option>
                        </select>
                    </div>
                    <div>
                        <button id="prevPage" disabled>上一页</button>
                        <span id="pageNumbers" style="margin: 0 10px;"></span>
                        <button id="nextPage" disabled>下一页</button>
                    </div>
                </div>
                <div class="preview-table-wrapper">
                    <table class="preview-table" id="previewTable">
                        <thead><tr>
                            <th>UT <input type="text" placeholder="过滤..." data-filter="UT"></th>
                            <th>Author <input type="text" placeholder="过滤..." data-filter="Author"></th>
                            <th>Institute <input type="text" placeholder="过滤..." data-filter="Institute"></th>
                            <th>Index <input type="text" placeholder="过滤..." data-filter="Index"></th>
                            <th>机构 <input type="text" placeholder="过滤..." data-filter="机构"></th>
                            <th>姓名 <input type="text" placeholder="过滤..." data-filter="姓名"></th>
                            <th>部门 <input type="text" placeholder="过滤..." data-filter="部门"></th>
                        </tr></thead>
                        <tbody id="previewBody"></tbody>
                    </table>
                </div>
            </div>
        </div>
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <div>正在处理...</div>
        </div>
    </div>

    <!-- Help Modal -->
    <div class="modal" id="helpModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>使用帮助</h2>
                <button class="modal-close" id="closeModal">&times;</button>
            </div>
            <div class="modal-body">
                <h3>功能说明</h3>
                <p>本工具用于解析Web of Science导出的TXT文件，自动匹配作者中文姓名和部门信息。</p>

                <h3>匹配逻辑</h3>
                <ul>
                    <li><strong>机构匹配</strong>：根据配置中的机构英文名，在作者机构信息中进行包含匹配（不区分大小写）。例如配置中"Jinling Inst"可匹配"Jinling Institute of Technology"。</li>
                    <li><strong>姓名匹配</strong>：精确匹配（不区分大小写）。配置中的英文名必须与WOS中的完全一致才能匹配。</li>
                    <li><strong>歧义消除</strong>：当一个英文名匹配到多个中文姓名时，优先从"已知信息"表中通过UT号消除歧义。如果该UT号下有匹配的中文姓名，则只取该姓名；否则用分号隔开返回所有匹配结果。</li>
                    <li><strong>部门匹配</strong>：根据中文姓名查找部门。当同一姓名可能有多个部门时，优先使用"已知信息"表中的UT+姓名精确匹配。</li>
                </ul>

                <h3>多值处理</h3>
                <p>当一个英文作者名匹配到多个中文姓名时，系统会尝试通过UT号消除歧义。如果无法消除歧义，则用英文分号<code>;</code>分隔，并以红色背景高亮显示。</p>

                <h3>配置文件格式</h3>
                <div class="example">
                    <p><strong>机构英中表：</strong>英文 → 中文（包含匹配）</p>
                    <p><strong>作者英中表：</strong>英文 → 中文（精确匹配，不区分大小写）</p>
                    <p><strong>作者部门表：</strong>中文姓名 → 部门</p>
                    <p><strong>已知信息表：</strong>UT + 中文姓名 → 部门（用于消除歧义）</p>
                </div>

                <h3>输出字段</h3>
                <ul>
                    <li><strong>UT</strong>：WOS唯一标识号</li>
                    <li><strong>Author</strong>：作者英文名</li>
                    <li><strong>Institute</strong>：机构英文名</li>
                    <li><strong>Index</strong>：作者序号</li>
                    <li><strong>机构</strong>：机构中文名（匹配结果）</li>
                    <li><strong>姓名</strong>：作者中文名（匹配结果）</li>
                    <li><strong>部门</strong>：作者部门（匹配结果）</li>
                </ul>
            </div>
        </div>
    </div>
    <script>
'''

# Add the base64 config
html_content += f'const DEFAULT_CONFIG_BASE64 = "{config_base64}";\n\n'

html_content += '''// Global state
let uploadedFiles = [];
let parsedData = [];
let appConfig = null;
let currentPage = 1;
let pageSize = 25;
let filters = {};

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const parseBtn = document.getElementById('parseBtn');
const clearBtn = document.getElementById('clearBtn');
const configArea = document.getElementById('configArea');
const configInput = document.getElementById('configInput');
const configStatus = document.getElementById('configStatus');
const downloadConfigBtn = document.getElementById('downloadConfigBtn');
const resetConfigBtn = document.getElementById('resetConfigBtn');
const resultCard = document.getElementById('resultCard');
const stats = document.getElementById('stats');
const resultInfo = document.getElementById('resultInfo');
const downloadBtn = document.getElementById('downloadBtn');
const previewBody = document.getElementById('previewBody');
const loading = document.getElementById('loading');
const pageSizeSelect = document.getElementById('pageSize');
const prevPageBtn = document.getElementById('prevPage');
const nextPageBtn = document.getElementById('nextPage');
const pageInfoText = document.getElementById('pageInfoText');
const pageNumbers = document.getElementById('pageNumbers');
const helpBtn = document.getElementById('helpBtn');
const helpModal = document.getElementById('helpModal');
const closeModal = document.getElementById('closeModal');

// Initialize default config on load
document.addEventListener('DOMContentLoaded', () => {
    loadDefaultConfig();
    setupFilterListeners();
    setupPaginationListeners();
    setupModalListeners();
});

// Load default config from base64
function loadDefaultConfig() {
    try {
        const binary = atob(DEFAULT_CONFIG_BASE64);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
        const workbook = XLSX.read(bytes, { type: 'array' });
        appConfig = parseConfigWorkbook(workbook);
        configStatus.className = 'config-status default';
        configStatus.textContent = '使用内置默认配置';
    } catch (e) {
        console.error('Failed to load default config:', e);
        appConfig = { institutions: [], authors: [], departments: [], knownInfo: [] };
    }
}

// Parse config workbook
function parseConfigWorkbook(workbook) {
    const config = { institutions: [], authors: [], departments: [], knownInfo: [] };
    const sheets = workbook.SheetNames;

    for (const name of sheets) {
        const sheet = workbook.Sheets[name];
        const data = XLSX.utils.sheet_to_json(sheet, { header: 1 });
        if (data.length < 2) continue;

        const headers = data[0];
        if (headers.length < 2) continue;

        const col0 = String(headers[0]).toLowerCase();
        const col1 = String(headers[1]).toLowerCase();

        if (col0.includes('英') && col1.includes('中')) {
            // Determine sheet type by checking first data row
            let isInstitutionSheet = false;
            if (data.length > 1 && data[1][0]) {
                const firstValue = String(data[1][0]).trim();
                // Institution names are typically longer and contain spaces, dots, or specific keywords
                // Author names are typically "Last, First" format and shorter
                isInstitutionSheet = firstValue.length > 15 ||
                    firstValue.toLowerCase().includes('inst') ||
                    firstValue.toLowerCase().includes('univ') ||
                    firstValue.toLowerCase().includes('college') ||
                    firstValue.toLowerCase().includes('school') ||
                    !firstValue.includes(',');
            }

            for (let i = 1; i < data.length; i++) {
                if (data[i][0] && data[i][1]) {
                    if (isInstitutionSheet) {
                        config.institutions.push({
                            english: String(data[i][0]).trim(),
                            chinese: String(data[i][1]).trim()
                        });
                    } else {
                        config.authors.push({
                            english: String(data[i][0]).trim(),
                            chinese: String(data[i][1]).trim()
                        });
                    }
                }
            }
        } else if (col0.includes('姓名') && col1.includes('部门')) {
            for (let i = 1; i < data.length; i++) {
                if (data[i][0] && data[i][1]) {
                    config.departments.push({
                        name: String(data[i][0]).trim(),
                        department: String(data[i][1]).trim()
                    });
                }
            }
        } else if (headers.length >= 3 && col0.toLowerCase() === 'ut') {
            for (let i = 1; i < data.length; i++) {
                if (data[i][0] && data[i][1] && data[i][2]) {
                    config.knownInfo.push({
                        ut: String(data[i][0]).trim(),
                        name: String(data[i][1]).trim(),
                        department: String(data[i][2]).trim()
                    });
                }
            }
        }
    }

    console.log('Config loaded:', config);
    return config;
}

// Upload area events
uploadArea.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => { handleFiles(e.target.files); fileInput.value = ''; });
uploadArea.addEventListener('dragover', (e) => { e.preventDefault(); uploadArea.classList.add('dragover'); });
uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('dragover'));
uploadArea.addEventListener('drop', (e) => { e.preventDefault(); uploadArea.classList.remove('dragover'); handleFiles(e.dataTransfer.files); });

// Config upload events
configArea.addEventListener('click', () => configInput.click());
configInput.addEventListener('change', (e) => { handleConfigFile(e.target.files[0]); configInput.value = ''; });
configArea.addEventListener('dragover', (e) => { e.preventDefault(); configArea.classList.add('dragover'); });
configArea.addEventListener('dragleave', () => configArea.classList.remove('dragover'));
configArea.addEventListener('drop', (e) => { e.preventDefault(); configArea.classList.remove('dragover'); handleConfigFile(e.dataTransfer.files[0]); });

// Handle files
function handleFiles(files) {
    const txtFiles = Array.from(files).filter(f => f.name.endsWith('.txt'));
    if (txtFiles.length === 0) { alert('请上传TXT格式的文件'); return; }
    uploadedFiles = [...uploadedFiles, ...txtFiles];
    updateFileList();
    updateButtons();
}

function updateFileList() {
    fileList.innerHTML = uploadedFiles.map((file, index) =>
        `<div class="file-item"><span class="file-name">📄 ${file.name}</span><span class="file-remove" onclick="removeFile(${index})">✕</span></div>`
    ).join('');
}

function removeFile(index) { uploadedFiles.splice(index, 1); updateFileList(); updateButtons(); }
function updateButtons() { parseBtn.disabled = uploadedFiles.length === 0; clearBtn.disabled = uploadedFiles.length === 0; }

clearBtn.addEventListener('click', () => { uploadedFiles = []; updateFileList(); updateButtons(); resultCard.classList.add('hidden'); });

// Handle config file
function handleConfigFile(file) {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            const workbook = XLSX.read(new Uint8Array(e.target.result), { type: 'array' });
            appConfig = parseConfigWorkbook(workbook);
            configStatus.className = 'config-status loaded';
            configStatus.textContent = `✓ 已加载自定义配置`;
        } catch (e) {
            alert('配置文件解析失败: ' + e.message);
        }
    };
    reader.readAsArrayBuffer(file);
}

// Download config template
downloadConfigBtn.addEventListener('click', () => {
    const wb = XLSX.utils.book_new();
    const instData = [['英文', '中文'], ['Jinling Inst', '金科院']];
    XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(instData), '机构英中');
    const authData = [['英文', '中文'], ['Zhao, Di', '赵迪'], ['Tong, Lili', '童丽丽']];
    XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(authData), '作者英中');
    const deptData = [['姓名', '部门'], ['刘志远', '校领导'], ['张三', '人事处']];
    XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(deptData), '作者部门');
    const knownData = [['UT', '姓名', '部门'], ['WOS:001064822400001', '陈晖', '人事处']];
    XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(knownData), '已知信息');
    XLSX.writeFile(wb, 'WOS配置模板.xlsx');
});

// Reset config
resetConfigBtn.addEventListener('click', loadDefaultConfig);

// Setup modal listeners
function setupModalListeners() {
    helpBtn.addEventListener('click', () => helpModal.classList.add('show'));
    closeModal.addEventListener('click', () => helpModal.classList.remove('show'));
    helpModal.addEventListener('click', (e) => {
        if (e.target === helpModal) helpModal.classList.remove('show');
    });
}

// Setup pagination listeners
function setupPaginationListeners() {
    pageSizeSelect.addEventListener('change', (e) => {
        pageSize = parseInt(e.target.value);
        currentPage = 1;
        renderTable();
    });
    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) { currentPage--; renderTable(); }
    });
    nextPageBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(getFilteredData().length / pageSize);
        if (currentPage < totalPages) { currentPage++; renderTable(); }
    });
}

// Setup filter listeners
function setupFilterListeners() {
    document.querySelectorAll('[data-filter]').forEach(input => {
        input.addEventListener('input', (e) => {
            const field = e.target.dataset.filter;
            filters[field] = e.target.value.toLowerCase();
            currentPage = 1;
            renderTable();
        });
    });
}

// Get filtered data
function getFilteredData() {
    return parsedData.filter(item => {
        for (const [field, value] of Object.entries(filters)) {
            if (!value) continue;
            const itemValue = String(item[field] || '').toLowerCase();
            if (!itemValue.includes(value)) return false;
        }
        return true;
    });
}

// Render table with pagination
function renderTable() {
    const filteredData = getFilteredData();
    const totalPages = Math.ceil(filteredData.length / pageSize);
    const start = (currentPage - 1) * pageSize;
    const end = Math.min(start + pageSize, filteredData.length);
    const pageData = filteredData.slice(start, end);

    // Update page info
    pageInfoText.textContent = `第 ${start + 1}-${end} 条，共 ${filteredData.length} 条`;

    // Update pagination buttons
    prevPageBtn.disabled = currentPage <= 1;
    nextPageBtn.disabled = currentPage >= totalPages;

    // Render page numbers
    let pageHtml = '';
    for (let i = 1; i <= totalPages && i <= 5; i++) {
        if (i === currentPage) {
            pageHtml += `<strong style="margin: 0 5px;">${i}</strong>`;
        } else {
            pageHtml += `<a href="#" onclick="goToPage(${i}); return false;" style="margin: 0 5px; color: #667eea;">${i}</a>`;
        }
    }
    if (totalPages > 5) pageHtml += ` ... ${totalPages}`;
    pageNumbers.innerHTML = pageHtml;

    // Render table rows
    previewBody.innerHTML = pageData.map(item => {
        const nameHighlight = item['姓名'] && item['姓名'].includes(';') ? 'highlight' : '';
        const deptHighlight = item['部门'] && item['部门'].includes(';') ? 'highlight' : '';
        return `<tr>
            <td>${escapeHtml(item.UT)}</td>
            <td>${escapeHtml(item.Author)}</td>
            <td title="${escapeHtml(item.Institute)}">${escapeHtml(item.Institute ? (item.Institute.length > 50 ? item.Institute.substring(0, 50) + '...' : item.Institute) : '')}</td>
            <td>${item.Index}</td>
            <td>${escapeHtml(item['机构'])}</td>
            <td class="${nameHighlight}">${escapeHtml(item['姓名'])}</td>
            <td class="${deptHighlight}">${escapeHtml(item['部门'])}</td>
        </tr>`;
    }).join('');
}

function goToPage(page) {
    currentPage = page;
    renderTable();
}

// Parse button
parseBtn.addEventListener('click', async () => {
    loading.style.display = 'block';
    resultCard.classList.add('hidden');

    try {
        const allResults = [];
        for (const file of uploadedFiles) {
            const text = await readFileAsText(file);
            const records = parseWOSText(text);
            allResults.push(...records);
        }

        const beforeDedup = allResults.length;
        parsedData = deduplicateData(allResults);
        displayResults(beforeDedup);
    } catch (error) {
        alert('解析错误: ' + error.message);
    } finally {
        loading.style.display = 'none';
    }
});

function readFileAsText(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = reject;
        reader.readAsText(file, 'UTF-8');
    });
}

// ========== 匹配函数 ==========

/**
 * 机构匹配函数
 * 使用包含匹配（不区分大小写）
 * 在机构英文名中查找配置的关键词，找到则返回对应中文名
 */
function matchInstitution(instituteEnglish) {
    if (!instituteEnglish || !appConfig.institutions.length) return '';
    const lower = instituteEnglish.toLowerCase();
    for (const inst of appConfig.institutions) {
        if (lower.includes(inst.english.toLowerCase())) {
            return inst.chinese;
        }
    }
    return '';
}

/**
 * 作者姓名标准化函数
 * 用于精确匹配前的预处理：转小写、合并多余空格
 */
function normalizeAuthorForMatch(name) {
    return name.toLowerCase().replace(/\\s+/g, ' ').trim();
}

/**
 * 作者姓名匹配函数
 * 精确匹配（不区分大小写）
 * 配置中的英文名必须与WOS中的完全一致才能匹配
 * 返回所有匹配到的中文名数组（可能有多个同名不同字的情况）
 */
function matchAuthorName(authorEnglish) {
    if (!authorEnglish || !appConfig.authors.length) return [];

    const results = [];
    const normalized = normalizeAuthorForMatch(authorEnglish);

    for (const auth of appConfig.authors) {
        const configNorm = normalizeAuthorForMatch(auth.english);

        // 精确匹配（不区分大小写）
        if (normalized === configNorm) {
            if (!results.includes(auth.chinese)) {
                results.push(auth.chinese);
            }
        }
    }

    return results;
}

/**
 * 中文姓名歧义消除函数
 * 当一个英文名匹配到多个中文姓名时：
 * 1. 先尝试从knownInfo表中通过UT号消除歧义
 * 2. 如果该UT号下有匹配的中文姓名，只返回该姓名
 * 3. 否则用分号隔开返回所有匹配结果
 */
function disambiguateNames(chineseNames, ut) {
    // 只有一个或没有匹配结果，直接返回
    if (!chineseNames || chineseNames.length <= 1) {
        return chineseNames.join('; ');
    }

    // 尝试从已知信息表中消除歧义
    if (ut && appConfig.knownInfo) {
        for (const info of appConfig.knownInfo) {
            if (info.ut === ut && chineseNames.includes(info.name)) {
                return info.name;  // 找到精确匹配，只返回该姓名
            }
        }
    }

    // 无法消除歧义，去重后用分号分隔返回所有结果
    return [...new Set(chineseNames)].join('; ');
}

/**
 * 部门匹配函数
 * 根据中文姓名查找部门
 * 优先从knownInfo表中通过UT+姓名精确匹配
 * 否则从部门表中查找
 */
function matchDepartment(authorChinese, ut) {
    if (!authorChinese) return '';

    // 拆分可能有多个姓名的情况（用分号分隔）
    const names = authorChinese.split(';').map(n => n.trim()).filter(n => n);
    const allDepts = [];

    for (const name of names) {
        const depts = [];

        // 优先从已知信息表中查找（UT + 姓名）
        if (ut && appConfig.knownInfo) {
            for (const info of appConfig.knownInfo) {
                if (info.ut === ut && info.name === name) {
                    depts.push(info.department);
                }
            }
        }

        // 如果已知信息表中没有，从部门表中查找
        if (depts.length === 0 && appConfig.departments) {
            for (const dept of appConfig.departments) {
                if (dept.name === name) {
                    depts.push(dept.department);
                }
            }
        }

        if (depts.length > 0) {
            allDepts.push(...depts);
        }
    }

    // 去重后用分号分隔返回
    const uniqueDepts = [...new Set(allDepts)];
    return uniqueDepts.join('; ');
}

// ========== WOS Parsing ==========

function parseWOSText(text) {
    const results = [];
    const lines = text.split('\\n');
    let currentRecord = null;
    let currentField = null;
    let fieldContent = [];

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmedLine = line.trim();

        if (trimmedLine === '' || trimmedLine === 'ER') {
            if (currentRecord) {
                if (currentField && fieldContent.length > 0) {
                    currentRecord[currentField] = fieldContent.join('\\n');
                }
                processRecord(currentRecord, results);
                currentRecord = null;
                currentField = null;
                fieldContent = [];
            }
            continue;
        }

        const fieldMatch = line.match(/^([A-Z0-9]{2})\\s+(.*)$/);

        if (fieldMatch) {
            if (currentField && fieldContent.length > 0) {
                currentRecord[currentField] = fieldContent.join('\\n');
            }
            const fieldName = fieldMatch[1];
            const fieldValue = fieldMatch[2];
            if (!currentRecord) currentRecord = {};
            currentField = fieldName;
            fieldContent = [fieldValue];
        } else if (line.startsWith('   ') && currentField) {
            fieldContent.push(trimmedLine);
        }
    }

    if (currentRecord) {
        if (currentField && fieldContent.length > 0) {
            currentRecord[currentField] = fieldContent.join('\\n');
        }
        processRecord(currentRecord, results);
    }

    return results;
}

/**
 * 处理单条WOS记录
 * 为每个作者生成一行结果，包含：
 * - UT: WOS唯一标识号
 * - Author: 作者英文名（来自AF字段）
 * - Institute: 作者所属机构英文名（来自C1字段）
 * - Index: 作者序号（第几作者）
 * - 机构: 机构中文名（匹配结果）
 * - 姓名: 作者中文名（匹配结果，可能需要消歧）
 * - 部门: 作者部门（匹配结果）
 */
function processRecord(record, results) {
    const ut = record['UT'];
    // AF字段包含作者全名列表，决定作者顺序
    const afList = (record['AF'] || '').split('\\n').map(a => a.trim()).filter(a => a);
    // C1字段包含作者-机构对应关系
    const c1Raw = record['C1'] || '';

    if (!ut || afList.length === 0) return;

    // 解析C1字段获取每个作者的机构信息
    const authorInstitutions = parseC1Field(c1Raw);

    // 为每个作者生成一行记录
    afList.forEach((author, index) => {
        const authorOrder = index + 1;
        // 查找该作者的具体机构
        const institution = findInstitution(author, authorInstitutions);
        // 匹配机构中文名（针对每个作者的具体机构）
        const instituteChinese = matchInstitution(institution);
        // 匹配作者中文名（精确匹配，可能有多个结果）
        const chineseNames = matchAuthorName(author);
        // 使用knownInfo消除歧义（通过UT号）
        const authorChinese = disambiguateNames(chineseNames, ut);
        // 匹配部门
        const department = matchDepartment(authorChinese, ut);

        results.push({
            UT: ut,
            Author: author,
            Institute: institution,
            Index: authorOrder,
            '机构': instituteChinese,
            '姓名': authorChinese,
            '部门': department
        });
    });
}

/**
 * 解析C1字段（作者-机构对应关系）
 * C1字段格式示例：[Wang, Xiaoming; Li, Qiang] Jinling Inst Technol, Nanjing, China.
 * 返回作者-机构映射数组：[{author: "Wang, Xiaoming", institution: "Jinling Inst Technol, Nanjing, China."}, ...]
 */
function parseC1Field(c1Text) {
    const authorInstitutions = [];
    const c1Lines = c1Text.split('\\n');
    let currentAuthors = [];
    let currentInstitution = '';

    for (const line of c1Lines) {
        // 匹配格式：[作者1; 作者2; ...] 机构名称
        const authorMatch = line.match(/^\\[([^\\]]+)\\]\\s*(.*)$/);

        if (authorMatch) {
            // 先保存前一组作者-机构关系
            if (currentAuthors.length > 0 && currentInstitution) {
                currentAuthors.forEach(author => {
                    authorInstitutions.push({
                        author: normalizeAuthorName(author),
                        institution: currentInstitution
                    });
                });
            }
            // 解析新的作者列表和机构
            const authorListStr = authorMatch[1];
            currentAuthors = authorListStr.split(';').map(a => a.trim()).filter(a => a);
            currentInstitution = authorMatch[2].trim();
        } else if (line.trim() && currentInstitution) {
            // 机构名称续行
            currentInstitution += ' ' + line.trim();
        }
    }

    // 保存最后一组作者-机构关系
    if (currentAuthors.length > 0 && currentInstitution) {
        currentAuthors.forEach(author => {
            authorInstitutions.push({
                author: normalizeAuthorName(author),
                institution: currentInstitution
            });
        });
    }

    return authorInstitutions;
}

/**
 * 标准化作者姓名格式
 * 去除首尾空格，合并多余空格
 */
function normalizeAuthorName(name) {
    return name.trim().replace(/\\s+/g, ' ');
}

function findInstitution(author, authorInstitutions) {
    const normalizedAuthor = normalizeAuthorName(author);

    for (const item of authorInstitutions) {
        if (item.author.toLowerCase() === normalizedAuthor.toLowerCase()) {
            return item.institution;
        }
    }

    const afParts = normalizedAuthor.split(',').map(p => p.trim());
    const afLastName = afParts[0].toLowerCase();
    const afFirstName = afParts[1] || '';

    for (const item of authorInstitutions) {
        const itemParts = item.author.split(',').map(p => p.trim());
        const itemLastName = (itemParts[0] || '').toLowerCase();
        const itemFirstName = itemParts[1] || '';

        if (itemLastName !== afLastName) continue;

        if (itemFirstName.length === 1) {
            if (afFirstName.toLowerCase().startsWith(itemFirstName.toLowerCase())) return item.institution;
        } else if (afFirstName.length === 1) {
            if (itemFirstName.toLowerCase().startsWith(afFirstName.toLowerCase())) return item.institution;
        } else if (itemFirstName.toLowerCase() === afFirstName.toLowerCase()) {
            return item.institution;
        }
    }

    for (const item of authorInstitutions) {
        const itemLastName = item.author.split(',')[0].trim().toLowerCase();
        if (itemLastName === afLastName) return item.institution;
    }

    if (authorInstitutions.length === 1) return authorInstitutions[0].institution;
    return '';
}

function deduplicateData(data) {
    const seen = new Set();
    const result = [];
    for (const item of data) {
        const key = `${item.UT}|${item.Author}|${item.Institute}|${item.Index}`;
        if (!seen.has(key)) { seen.add(key); result.push(item); }
    }
    return result;
}

// ========== Display Results ==========

function displayResults(beforeDedup) {
    const recordCount = new Set(parsedData.map(d => d.UT)).size;
    const authorCount = parsedData.length;

    let matchedInst = 0, matchedName = 0, matchedDept = 0;
    for (const item of parsedData) {
        if (item['机构']) matchedInst++;
        if (item['姓名']) matchedName++;
        if (item['部门']) matchedDept++;
    }

    stats.innerHTML = `
        <div class="stat-item"><div class="stat-number">${uploadedFiles.length}</div><div class="stat-label">文件数</div></div>
        <div class="stat-item"><div class="stat-number">${recordCount}</div><div class="stat-label">记录数</div></div>
        <div class="stat-item"><div class="stat-number">${authorCount}</div><div class="stat-label">作者数</div></div>
        <div class="stat-item"><div class="stat-number">${matchedName}</div><div class="stat-label">姓名匹配</div></div>
        <div class="stat-item"><div class="stat-number">${matchedDept}</div><div class="stat-label">部门匹配</div></div>
    `;

    resultInfo.textContent = `解析完成！去重后 ${authorCount} 条记录，姓名匹配 ${matchedName} 条，部门匹配 ${matchedDept} 条`;

    // Reset filters and pagination
    filters = {};
    currentPage = 1;
    document.querySelectorAll('[data-filter]').forEach(input => input.value = '');

    // Render table
    renderTable();
    resultCard.classList.remove('hidden');
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ========== Download Excel ==========

downloadBtn.addEventListener('click', () => {
    if (parsedData.length === 0) return;

    const headers = ['UT', 'Author', 'Institute', 'Index', '机构', '姓名', '部门'];
    const data = [headers];

    for (const item of parsedData) {
        data.push([
            item.UT, item.Author, item.Institute, item.Index,
            item['机构'], item['姓名'], item['部门']
        ]);
    }

    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(data);

    ws['!cols'] = [
        { wch: 25 }, { wch: 20 }, { wch: 60 }, { wch: 6 },
        { wch: 10 }, { wch: 15 }, { wch: 20 }
    ];

    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');

    const recordCount = new Set(parsedData.map(d => d.UT)).size;
    const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const filename = `WOS解析结果_${recordCount}条_${timestamp}.xlsx`;

    XLSX.writeFile(wb, filename);
});
    </script>
</body>
</html>
'''

# Write the file
with open('wos-parser-enhanced.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Enhanced WOS parser created: wos-parser-enhanced.html")
print(f"Config base64 length: {len(config_base64)}")
