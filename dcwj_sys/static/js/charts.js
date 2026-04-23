// 图表初始化脚本
// 使用 Chart.js 库

// 初始化图表
function initChart(canvasId, type, labels, data, title) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: data,
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(118, 75, 162, 0.8)',
                    'rgba(237, 100, 166, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(231, 233, 237, 0.8)'
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(118, 75, 162, 1)',
                    'rgba(237, 100, 166, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(231, 233, 237, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: type === 'pie',
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: title
                }
            },
            scales: type === 'bar' ? {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            } : {}
        }
    });
}

// 确认删除
function confirmDelete(message) {
    return confirm(message);
}

// AJAX 请求封装
function ajaxRequest(url, method, data, successCallback, errorCallback) {
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => response.json())
    .then(data => {
        if (successCallback) successCallback(data);
    })
    .catch(error => {
        if (errorCallback) errorCallback(error);
    });
}

// 动态添加问题（管理后台使用）
let questionCount = 0;

function addQuestion() {
    const container = document.getElementById('questions-container');
    if (!container) return;

    const questionDiv = document.createElement('div');
    questionDiv.className = 'question-item';
    questionDiv.id = `question-${questionCount}`;
    questionDiv.innerHTML = `
        <div class="form-group">
            <label class="form-label">问题内容 (中文) *</label>
            <input type="text" name="question_text_zh_${questionCount}" class="form-control" required>
        </div>
        <div class="form-group">
            <label class="form-label">问题内容 (English)</label>
            <input type="text" name="question_text_en_${questionCount}" class="form-control">
        </div>
        <div class="form-group">
            <label class="form-label">问题类型</label>
            <select name="question_type_${questionCount}" class="form-control" onchange="handleQuestionTypeChange(${questionCount}, this.value)">
                <option value="single">单选题</option>
                <option value="multiple">多选题</option>
                <option value="text">填空题</option>
                <option value="rating">评分题</option>
            </select>
        </div>
        <div class="form-group">
            <label>
                <input type="checkbox" name="is_required_${questionCount}">
                是否必填
            </label>
        </div>
        <div id="options-container-${questionCount}" class="options-container">
            <button type="button" class="btn btn-sm btn-secondary" onclick="addOption(${questionCount})">添加选项</button>
        </div>
        <div class="form-group" id="max-length-${questionCount}" style="display:none;">
            <label class="form-label">最大字符数</label>
            <input type="number" name="max_length_${questionCount}" class="form-control" value="500">
        </div>
        <div class="form-group" id="rating-scale-${questionCount}" style="display:none;">
            <label class="form-label">评分范围</label>
            <select name="rating_scale_${questionCount}" class="form-control">
                <option value="5">1-5分</option>
                <option value="10">1-10分</option>
            </select>
        </div>
        <button type="button" class="btn btn-sm btn-danger" onclick="removeQuestion(${questionCount})">删除问题</button>
        <hr>
    `;

    container.appendChild(questionDiv);

    // 默认添加两个选项
    addOption(questionCount);
    addOption(questionCount);

    questionCount++;
    updateQuestionCount();
}

function removeQuestion(index) {
    const questionDiv = document.getElementById(`question-${index}`);
    if (questionDiv) {
        questionDiv.remove();
    }
}

function handleQuestionTypeChange(questionIndex, type) {
    const optionsContainer = document.getElementById(`options-container-${questionIndex}`);
    const maxLengthDiv = document.getElementById(`max-length-${questionIndex}`);
    const ratingScaleDiv = document.getElementById(`rating-scale-${questionIndex}`);

    if (type === 'single' || type === 'multiple') {
        optionsContainer.style.display = 'block';
    } else {
        optionsContainer.style.display = 'none';
    }

    if (type === 'text') {
        maxLengthDiv.style.display = 'block';
    } else {
        maxLengthDiv.style.display = 'none';
    }

    if (type === 'rating') {
        ratingScaleDiv.style.display = 'block';
    } else {
        ratingScaleDiv.style.display = 'none';
    }
}

let optionCounts = {};

function addOption(questionIndex) {
    if (!optionCounts[questionIndex]) {
        optionCounts[questionIndex] = 0;
    }

    const container = document.getElementById(`options-container-${questionIndex}`);
    if (!container) return;

    const optionDiv = document.createElement('div');
    optionDiv.className = 'option-item';
    optionDiv.id = `option-${questionIndex}-${optionCounts[questionIndex]}`;
    optionDiv.innerHTML = `
        <div class="form-group">
            <label class="form-label">选项 (中文) *</label>
            <input type="text" name="option_text_zh_${questionIndex}_${optionCounts[questionIndex]}" class="form-control" required>
        </div>
        <div class="form-group">
            <label class="form-label">选项 (English)</label>
            <input type="text" name="option_text_en_${questionIndex}_${optionCounts[questionIndex]}" class="form-control">
        </div>
        <button type="button" class="btn btn-sm btn-danger" onclick="removeOption(${questionIndex}, ${optionCounts[questionIndex]})">删除选项</button>
    `;

    // 在按钮前插入
    const addButton = container.querySelector('button');
    container.insertBefore(optionDiv, addButton);

    optionCounts[questionIndex]++;
    updateOptionCount(questionIndex);
}

function removeOption(questionIndex, optionIndex) {
    const optionDiv = document.getElementById(`option-${questionIndex}-${optionIndex}`);
    if (optionDiv) {
        optionDiv.remove();
    }
}

function updateQuestionCount() {
    const input = document.getElementById('question_count');
    if (input) {
        input.value = questionCount;
    }
}

function updateOptionCount(questionIndex) {
    const input = document.getElementById(`option_count_${questionIndex}`);
    if (input) {
        input.value = optionCounts[questionIndex];
    } else {
        // 创建隐藏字段
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.id = `option_count_${questionIndex}`;
        hiddenInput.name = `option_count_${questionIndex}`;
        hiddenInput.value = optionCounts[questionIndex];
        document.querySelector('form').appendChild(hiddenInput);
    }
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 自动隐藏提示消息
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});
