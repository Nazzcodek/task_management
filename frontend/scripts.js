$(document).ready(function () {
    function loadTasks() {
        $.ajax({
            url: '/api/v1/tasks/',
            method: 'GET',
            success: function (data) {
                $('#tasks').empty();
                data.forEach(task => {
                    $('#tasks').append(`
                        <div class="bg-white p-4 rounded shadow-md" data-id="${task.id}">
                            <h3 class="text-xl font-semibold">${task.title}</h3>
                            <p>${task.description}</p>
                            <div class="flex justify-between mt-4">
                                <span class="bg-gray-200 text-gray-700 p-1 rounded">${task.priority}</span>
                                <span class="bg-gray-200 text-gray-700 p-1 rounded">${task.status}</span>
                            </div>
                        </div>
                    `);
                });
            }
        });
    }

    function openModal() {
        $('#taskModal').removeClass('hidden');
    }

    function closeModal() {
        $('#taskModal').addClass('hidden');
    }

    $('#addTask').on('click', function () {
        openModal();
    });

    $('#closeModal').on('click', function () {
        closeModal();
    });

    $('#taskForm').on('submit', function (e) {
        e.preventDefault();
        const taskId = $('#taskId').val();
        const taskData = {
            title: $('#taskTitle').val(),
            description: $('#taskDescription').val(),
            status: $('#taskStatus').val(),
            priority: $('#taskPriority').val(),
            due_date: $('#taskDueDate').val(),
            category: $('#taskCategory').val()
        };

        if (taskId) {
            $.ajax({
                url: `/api/v1/tasks/${taskId}/`,
                method: 'PUT',
                data: taskData,
                success: function () {
                    closeModal();
                    loadTasks();
                }
            });
        } else {
            $.ajax({
                url: '/api/v1/tasks/',
                method: 'POST',
                data: taskData,
                success: function () {
                    closeModal();
                    loadTasks();
                }
            });
        }
    });

    $('#filterTasks').on('click', function () {
        const priority = $('#priority').val();
        const category = $('#category').val();
        const due_date = $('#due_date').val();

        $.ajax({
            url: '/api/tasks/',
            method: 'GET',
            data: {
                priority: priority,
                category: category,
                due_date: due_date
            },
            success: function (data) {
                $('#tasks').empty();
                data.forEach(task => {
                    $('#tasks').append(`
                        <div class="bg-white p-4 rounded shadow-md" data-id="${task.id}">
                            <h3 class="text-xl font-semibold">${task.title}</h3>
                            <p>${task.description}</p>
                            <div class="flex justify-between mt-4">
                                <span class="bg-gray-200 text-gray-700 p-1 rounded">${task.priority}</span>
                                <span class="bg-gray-200 text-gray-700 p-1 rounded">${task.status}</span>
                            </div>
                        </div>
                    `);
                });
            }
        });
    });

    $('#search').on('keyup', function () {
        const query = $(this).val();

        $.ajax({
            url: '/api/v1/tasks/',
            method: 'GET',
            data: {
                search: query
            },
            success: function (data) {
                $('#tasks').empty();
                data.forEach(task => {
                    $('#tasks').append(`
                        <div class="bg-white p-4 rounded shadow-md" data-id="${task.id}">
                            <h3 class="text-xl font-semibold">${task.title}</h3>
                            <p>${task.description}</p>
                            <div class="flex justify-between mt-4">
                                <span class="bg-gray-200 text-gray-700 p-1 rounded">${task.priority}</span>
                                <span class="bg-gray-200 text-gray-700 p-1 rounded">${task.status}</span>
                            </div>
                        </div>
                    `);
                });
            }
        });
    });

    new Sortable(document.getElementById('tasks'), {
        group: 'tasks',
        animation: 150,
        onEnd: function (evt) {
            const taskId = $(evt.item).data('id');
            const newStatus = $(evt.to).data('status');

            $.ajax({
                url: `/api/v1/tasks/${taskId}/`,
                method: 'PUT',
                data: {
                    status: newStatus
                },
                success: function () {
                    loadTasks();
                }
            });
        }
    });

    loadTasks();
});
