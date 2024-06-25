$(document).ready(function () {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');

    if (token) {
        localStorage.setItem('authToken', token);
    } else {
        console.error("No token found in the URL");
    }

    $.ajaxSetup({
        /**
         * Sets the Authorization header in the AJAX request before it is sent.
         *
         * @param {XMLHttpRequest} xhr - The XMLHttpRequest object.
         * @param {Object} settings - The settings for the AJAX request.
         * @return {void} This function does not return anything.
         */
        beforeSend: function (xhr, settings) {
            const token = localStorage.getItem('authToken');
            if (token) {
                xhr.setRequestHeader('Authorization', 'Token ' + token);
            } else {
                console.error("No authToken found in localStorage");
            }
        }
    });

    /**
     * Retrieves a cookie value by name from the document's cookies.
     *
     * @param {string} name - The name of the cookie to retrieve.
     * @return {string} The value of the cookie with the specified name.
     */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    document.getElementById('addUserBtn').addEventListener('click', function() {
        document.getElementById('addUserModal').classList.toggle('hidden');
    });
    
    document.getElementById('cancelButton').addEventListener('click', function() {
        document.getElementById('addUserModal').classList.add('hidden');
    });
    
    document.getElementById('submitUser').addEventListener('click', async function() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
    
        try {
            const response = await $.ajax({
                url: '/api/v1/users/add_user/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ username, password }),
                dataType: 'json',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
    
            document.getElementById('addUserModal').classList.add('hidden');
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
    
            // Reload the page to reflect the newly added user
            window.location.reload();
        } catch (error) {
            console.error('Error adding user:', error);
    
            // Check for detailed error messages
            let errorMessage = 'An error occurred. Please try again.';
            if (error.responseJSON && error.responseJSON.error) {
                errorMessage = error.responseJSON.error;
                if (error.responseJSON.details) {
                    errorMessage += ': ' + Object.values(error.responseJSON.details).join(', ');
                }
            }
            
            document.getElementById('errorMessage').innerText = errorMessage;
            document.getElementById('errorMessage').classList.remove('hidden');
        }
    });
    
    let usersData = [];

/**
 * Fetches user information from the API and updates the UI.
 *
 * @return {Promise<void>} A promise that resolves when the function is complete.
 */
    const fetchUsers = async () => {
        try {
            const response = await $.ajax({
                url: '/api/v1/users/get_user_info/',
                method: 'GET',
            });
    
            console.log('API response:', response); // Add this line to log the response
    
            if (response && response.users && Array.isArray(response.users)) {
                usersData = response.users;
    
                // Display avatars next to the "Add Task" button
                const userAvatars = usersData.map(user => {
                    const initials = user.username.slice(0, 2).toUpperCase();
                    return `<img src="https://ui-avatars.com/api/?name=${initials}&background=random" alt="Avatar" class="w-8 h-8 rounded-full border-2 border-white">`;
                }).join('');
                $('#user-avatars').html(userAvatars);
    
                const remainingCount = response.total - response.users.length;
                if (remainingCount > 0) {
                    $('#user-avatars').append(`<span class="w-8 h-8 rounded-full bg-gray-300 text-white flex items-center justify-center">+${remainingCount}</span>`);
                }
    
                const assignToOptions = response.users.map(user => `<option value="${user.id}">${user.username}</option>`).join('');
                $('#taskAssignee').html(assignToOptions);
            } else {
                console.error('Invalid response structure:', response);
            }
        } catch (error) {
            console.error('Failed to fetch users:', error);
        }
    };
    

    /**
     * Asynchronously loads tasks from the server and populates the task cards based on their status.
     */
    const loadTasks = async () => {
        try {
            const response = await $.ajax({
                url: '/api/v1/tasks/',
                method: 'GET',
            });

            $('#in-progress-tasks, #completed-tasks, #over-due-tasks').empty();

            response.forEach(task => {
                const priorityColor = getPriorityColor(task.priority);
                const formattedDueDate = formatDueDate(task.due_date);
                const categoryColor = `hsl(${Math.random() * 360}, 100%, 30%)`;

                // Generate avatars for the task card based on assigned users
                const assignedUser = usersData.find(user => user.id === task.assigned_to);
                const initials = assignedUser ? assignedUser.username.slice(0, 2).toUpperCase() : 'NA';
                const userAvatar = `<img src="https://ui-avatars.com/api/?name=${initials}&background=random" alt="Avatar" class="w-8 h-8 rounded-full border-2 border-white">`;

                const taskCard = `
                    <div class="mb-1 p-2 flex justify-between">
                        <span class="inline-flex flex-grow bg-gray-50 shadow-md py-2 px-4 justify-center items-center text-sm" style="color: ${priorityColor};">${task.priority}</span>
                        <span class="inline-flex flex-grow bg-gray-50 shadow-md mx-4 py-2 px-4 justify-center items-center text-blue-500 text-sm">${formattedDueDate}</span>
                        <span class="inline-flex flex-grow bg-gray-50 shadow-md py-2 px-4 justify-center items-center text-sm" style="color: ${categoryColor};">${task.category}</span>
                    </div>
                    <div class="bg-gray-50 pt-2 pb-2 px-6 py-12 rounded shadow-md" data-id="${task.id}">
                        <h3 class="text-xl font-semibold">${task.title}</h3>
                        <p class="truncate">${task.description}</p>
                        <div class="flex justify-between items-center mt-4">
                            <div class="flex -space-x-2">${userAvatar}</div>
                            <div class="flex space-x-2">
                                <button class="preview-task text-black hover:text-blue-500" data-id="${task.id}"><i class="fas fa-eye"></i></button>
                                <button class="delete-task text-black hover:text-blue-500" data-id="${task.id}"><i class="fas fa-trash-alt"></i></button>
                                <button class="edit-task text-black hover:text-blue-500" data-id="${task.id}"><i class="fas fa-edit"></i></button>
                            </div>
                        </div>
                    </div>
                `;

                if (task.status === 'In Progress') {
                    $('#in-progress-tasks').append(taskCard);
                } else if (task.status === 'Completed') {
                    $('#completed-tasks').append(taskCard);
                } else if (task.status === 'Overdue') {
                    $('#over-due-tasks').append(taskCard);
                }
            });

            updateTaskCounts(response);
        } catch (error) {
            console.error('Failed to load tasks:', error);
        }
    };

    /**
     * Returns the corresponding color for a given priority.
     *
     * @param {string} priority - The priority level.
     * @return {string} The color corresponding to the priority level.
     */
    const getPriorityColor = (priority) => {
        switch (priority) {
            case 'High':
                return 'red';
            case 'Medium':
                return 'amber';
            case 'Low':
                return 'green';
            default:
                return '';
        }
    };

    /**
     * Formats a due date based on the current time.
     *
     * @param {string} dueDate - The due date in string format.
     * @return {string} The formatted due date.
     */
    const formatDueDate = (dueDate) => {
        const dueDateObj = new Date(dueDate);
        const now = new Date();
        const diffHours = Math.abs(dueDateObj - now) / 36e5;

        if (diffHours < 24) {
            return dueDateObj.toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
        } else if (diffHours < 48) {
            return 'Tomorrow';
        } else {
            return dueDateObj.toLocaleDateString('en-GB');
        }
    };

    /**
     * Updates the task counts displayed on the page.
     *
     * @param {Array<Object>} tasks - An array of task objects.
     * @return {void}
     */
    const updateTaskCounts = (tasks) => {
        const inProgressCount = countTasks('In Progress', tasks);
        const completedCount = countTasks('Completed', tasks);
        const overdueCount = countTasks('Overdue', tasks);

        updateTaskCount('in-progress-title', inProgressCount);
        updateTaskCount('completed-title', completedCount);
        updateTaskCount('over-due-title', overdueCount);
    };

    /**
     * Counts the number of tasks with a given status.
     *
     * @param {string} status - The status to filter by.
     * @param {Array<Object>} tasks - The array of tasks to count.
     * @return {number} The count of tasks with the given status.
     */
    const countTasks = (status, tasks) => {
        return tasks.filter(task => task.status === status).length;
    };

    /**
     * Updates the task count displayed on the page.
     *
     * @param {string} id - The ID of the element to update.
     * @param {number} count - The new count value.
     * @return {void}
     */
    const updateTaskCount = (id, count) => {
        $(`#${id}`).text(`${capitalize(id.split('-').join(' '))} (${count})`);
    };

    /**
     * Capitalizes the first letter of a string.
     *
     * @param {string} str - The string to capitalize.
     * @return {string} The capitalized string.
     */
    const capitalize = (str) => {
        return str.charAt(0).toUpperCase() + str.slice(1);
    };

        const openModal = () => {
            $('#taskModal').removeClass('hidden');
        };

    /**
     * Closes the task modal by adding the 'hidden' class to the '#taskModal' element and resetting the '#taskForm' form.
     *
     * @return {void} This function does not return anything.
     */
    const closeModal = () => {
        $('#taskModal').addClass('hidden');
        $('#taskForm')[0].reset();
    };

    $('#addTask').on('click', openModal);
    $('#closeModal').on('click', closeModal);

    $('#taskForm').on('submit', async function (e) {
        e.preventDefault();

        const taskId = $('#taskId').val();
        const taskData = {
            title: $('#taskTitle').val(),
            description: $('#taskDescription').val(),
            status: $('#taskStatus').val(),
            priority: $('#taskPriority').val(),
            due_date: $('#taskDueDate').val(),
            category: $('#taskCategory').val(),
            assigned_to: $('#taskAssignee').val(),
        };

        console.log('Submitting task data:', taskData);

        try {
            if (taskId) {
                await $.ajax({
                    url: `/api/v1/tasks/${taskId}/`,
                    method: 'PUT',
                    contentType: 'application/json',
                    data: JSON.stringify(taskData),
                });
            } else {
                await $.ajax({
                    url: '/api/v1/tasks/',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(taskData),
                });
            }
            closeModal();
            loadTasks();
        } catch (error) {
            console.error(`Failed to ${taskId ? 'update' : 'create'} task:`, error);
        }
    });

    $('#filterTasks').on('click', async function () {
        const priority = $('#priority').val();
        const category = $('#category').val();
        const due_date = $('#due_date').val();
        const sortOption = $('#sortOption').val();
    
        try {
            const data = await $.ajax({
                url: '/api/v1/tasks/',
                method: 'GET',
                data: { priority, category, due_date, sort: sortOption },
            });
            populateTasks(data);
        } catch (error) {
            console.error('Failed to filter tasks:', error);
        }
    });

    $('#search').on('keyup', async function () {
        const query = $(this).val();

        try {
            const data = await $.ajax({
                url: '/api/v1/tasks/',
                method: 'GET',
                data: { search: query },
            });
            populateTasks(data);
        } catch (error) {
            console.error('Failed to search tasks:', error);
        }
    });

    /**
     * Populates the task cards based on the provided tasks.
     *
     * @param {Array} tasks - An array of task objects to populate the task cards with.
     * @return {void} This function does not return anything.
     */
    const populateTasks = (tasks) => {
        $('#in-progress-tasks, #completed-tasks, #over-due-tasks').empty();

        tasks.forEach(task => {
            const priorityColor = getPriorityColor(task.priority);
            const formattedDueDate = formatDueDate(task.due_date);
            const categoryColor = `hsl(${Math.random() * 360}, 100%, 30%)`;

            // Generate avatars for the task card based on assigned users
            const assignedUser = usersData.find(user => user.id === task.assigned_to);
            const initials = assignedUser ? assignedUser.username.slice(0, 2).toUpperCase() : 'NA';
            const userAvatar = `<img src="https://ui-avatars.com/api/?name=${initials}&background=random" alt="Avatar" class="w-8 h-8 rounded-full border-2 border-white">`;


            const taskCard = `
                <div class="p-2 flex justify-between">
                    <span class="inline-flex flex-grow bg-gray-50 shadow-md py-2 px-4 justify-center items-center text-sm" style="color: ${priorityColor};">${task.priority}</span>
                    <span class="inline-flex flex-grow bg-gray-50 shadow-md mx-4 py-2 px-4 justify-center items-center text-blue-500 text-sm">${formattedDueDate}</span>
                    <span class="inline-flex flex-grow bg-gray-50 shadow-md py-2 px-4 justify-center items-center text-sm" style="color: ${categoryColor};">${task.category}</span>
                </div>
                <div class="bg-gray-50 p-4 rounded shadow-md" data-id="${task.id}">
                    <h3 class="text-xl font-semibold">${task.title}</h3>
                    <p class="truncate">${task.description}</p>
                    <div class="flex justify-between items-center mt-4">
                        <div class="flex -space-x-2">${userAvatar}</div>
                        <div class="flex space-x-2">
                            <button class="preview-task text-black hover:text-blue-500" data-id="${task.id}"><i class="fas fa-eye"></i></button>
                            <button class="delete-task text-black hover:text-blue-500" data-id="${task.id}"><i class="fas fa-trash-alt"></i></button>
                            <button class="edit-task text-black hover:text-blue-500" data-id="${task.id}"><i class="fas fa-edit"></i></button>
                        </div>
                    </div>
                </div>
            `;

            if (task.status === 'In Progress') {
                $('#in-progress-tasks').append(taskCard);
            } else if (task.status === 'Completed') {
                $('#completed-tasks').append(taskCard);
            } else if (task.status === 'Overdue') {
                $('#over-due-tasks').append(taskCard);
            }
        });

        updateTaskCounts(tasks);
    };

    $(document).on('click', '.delete-task', async function () {
        const taskId = $(this).data('id');
        const confirmation = confirm("Are you sure you want to delete this task?");

        if (confirmation) {
            try {
                await $.ajax({
                    url: `/api/v1/tasks/${taskId}/`,
                    method: 'DELETE',
                });
                loadTasks();
            } catch (error) {
                console.error('Failed to delete task:', error);
            }
        }
    });

    $(document).on('click', '.edit-task', async function () {
        const taskId = $(this).data('id');
        
        try {
            const task = await $.ajax({
                url: `/api/v1/tasks/${taskId}/`,
                method: 'GET',
            });

            $('#taskId').val(task.id);
            $('#taskTitle').val(task.title);
            $('#taskDescription').val(task.description);
            $('#taskStatus').val(task.status);
            $('#taskPriority').val(task.priority);
            $('#taskDueDate').val(task.due_date);
            $('#taskCategory').val(task.category);
            $('#taskAssignee').val(task.assigned_to);
            
            openModal();
        } catch (error) {
            console.error('Failed to fetch task:', error);
        }
    });

    $(document).on('click', '.preview-task', async function () {
        const taskId = $(this).data('id');
        
        try {
            const task = await $.ajax({
                url: `/api/v1/tasks/${taskId}/`,
                method: 'GET',
            });

            $('#taskTitle').val(task.title).attr('readonly', true);
            $('#taskDescription').val(task.description).attr('readonly', true);
            $('#taskStatus').val(task.status).attr('readonly', true);
            $('#taskPriority').val(task.priority).attr('readonly', true);
            $('#taskDueDate').val(task.due_date).attr('readonly', true);
            $('#taskCategory').val(task.category).attr('readonly', true);
            $('#taskAssignee').val(task.assigned_to).attr('readonly', true);
            
            openModal();
        } catch (error) {
            console.error('Failed to fetch task:', error);
        }
    });

    new Sortable(document.getElementById('in-progress-tasks'), {
        group: 'tasks',
        animation: 150,
        onEnd: function (evt) {
            const newStatus = determineStatusBasedOnColumn(evt.to.id);
            updateTaskStatus(evt.item, newStatus);
        }
    });

    new Sortable(document.getElementById('completed-tasks'), {
        group: 'tasks',
        animation: 150,
        onEnd: function (evt) {
            const newStatus = determineStatusBasedOnColumn(evt.to.id);
            updateTaskStatus(evt.item, newStatus);
        }
    });

    new Sortable(document.getElementById('over-due-tasks'), {
        group: 'tasks',
        animation: 150,
        onEnd: function (evt) {
            const newStatus = determineStatusBasedOnColumn(evt.to.id);
            updateTaskStatus(evt.item, newStatus);
        }
    });

    /**
     * Determines the status based on the column ID.
     *
     * @param {string} columnId - The ID of the column.
     * @return {string} The corresponding status based on the column ID.
     */
    const determineStatusBasedOnColumn = (columnId) => {
        switch (columnId) {
            case 'in-progress-tasks':
                return 'In Progress';
            case 'completed-tasks':
                return 'Completed';
            case 'over-due-tasks':
                return 'Overdue';
            default:
                return 'Unknown';
        }
    };

    /**
     * Updates the status of a task.
     *
     * @param {HTMLElement} taskElement - The HTML element representing the task.
     * @param {string} newStatus - The new status to be assigned to the task.
     * @return {Promise<void>} A Promise that resolves when the task status is updated.
     */
    const updateTaskStatus = async (taskElement, newStatus) => {
        const taskId = $(taskElement).data('id');

        try {
            await $.ajax({
                url: `/api/v1/tasks/${taskId}/`,
                method: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify({ status: newStatus }),
            });
            loadTasks();
        } catch (error) {
            console.error('Failed to update task status:', error);
        }
    };

    fetchUsers();
    loadTasks();
});
