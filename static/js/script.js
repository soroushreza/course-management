document.addEventListener('DOMContentLoaded', function() {
    const departmentSelect = document.getElementById('department-select');
    const coursesTable = document.getElementById('courses-table');
    const coursesTbody = document.getElementById('courses-tbody');
    const enrolledCoursesTbody = document.getElementById('enrolled-courses-tbody');
    const totalUnitsSpan = document.getElementById('total-units');
    const maxUnitsSpan = document.getElementById('max-units');
    const searchInput = document.getElementById('search-input');


        // تابع لود کردن دروس دانشکده
    function loadDepartmentCourses() {
        const departmentId = departmentSelect.value;
        if (departmentId) {
            fetch(`/get-department-courses/?department_id=${departmentId}`)
                .then(response => response.json())
                .then(data => {
                    coursesTbody.innerHTML = '';
                    coursesTable.style.display = 'table';
                    
                    data.courses.forEach(course => {
                        const row = document.createElement('tr');
                        let scheduleText = course.schedules.map(s => `${s.day}: ${s.start_time} - ${s.end_time}`).join('<br>');

                        row.innerHTML = `
                            <td>${course.code}</td>
                            <td>${course.name}</td>
                            <td>${course.credits}</td>
                            <td>${course.instructor__first_name} ${course.instructor__last_name}</td>
                            <td>${course.capacity}/${course.initial_capacity}</td>
                            <td>${scheduleText || 'نامشخص'}</td>
                            <td>${course.exam_date}</td>
                            <td>
                                <button class="btn btn-primary btn-sm" 
                                        data-course-id="${course.id}">
                                    انتخاب درس
                                </button>
                            </td>
                        `;
                        coursesTbody.appendChild(row);
                    });

                    // اضافه کردن event listeners
                    document.querySelectorAll('#courses-tbody [data-course-id]').forEach(button => {
                        button.addEventListener('click', enrollCourse);
                    });

                    loadEnrolledCourses();
                });
        } else {
            coursesTable.style.display = 'none';
        }
    }



    // آپدیت تابع loadEnrolledCourses
    function loadEnrolledCourses() {
        fetch('/get-enrolled-courses/')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    enrolledCoursesTbody.innerHTML = '';
                    data.courses.forEach(course => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${course.code}</td>
                            <td>${course.name}</td>
                            <td>${course.credits}</td>
                            <td>${course.instructor}</td>
                            <td>
                                <button class="btn btn-danger btn-sm drop-btn" 
                                        data-course-id="${course.id}">
                                    حذف درس
                                </button>
                            </td>
                        `;
                        enrolledCoursesTbody.appendChild(row);
                    });

                    // به‌روزرسانی تعداد واحدها
                    totalUnitsSpan.textContent = data.total_units;
                    maxUnitsSpan.textContent = data.max_units;
                    
                    // تغییر رنگ در صورت نزدیک شدن به سقف واحد
                    if (data.total_units > data.max_units * 0.8) {
                        totalUnitsSpan.classList.add('text-warning');
                    } else {
                        totalUnitsSpan.classList.remove('text-warning');
                    }

                    // اضافه کردن event listeners برای دکمه‌های حذف
                    document.querySelectorAll('.drop-btn').forEach(button => {
                        button.addEventListener('click', dropCourse);
                    });

                    updateEnrollButtons(data.courses);
                }
            })
            .catch(error => {
                console.error('Error loading enrolled courses:', error);
                showNotification('خطا در بارگیری دروس', 'error');
            });
    }

    // تابع به‌روزرسانی دکمه‌ها
    function updateEnrollButtons(enrolledCourses) {
        const enrolledIds = enrolledCourses.map(course => course.id);
        document.querySelectorAll('#courses-tbody [data-course-id]').forEach(button => {
            const courseId = parseInt(button.dataset.courseId);
            if (enrolledIds.includes(courseId)) {
                button.classList.remove('btn-primary');
                button.classList.add('btn-danger');
                button.textContent = 'حذف درس';
                button.removeEventListener('click', enrollCourse);
                button.addEventListener('click', dropCourse);
            } else {
                button.classList.remove('btn-danger');
                button.classList.add('btn-primary');
                button.textContent = 'انتخاب درس';
                button.removeEventListener('click', dropCourse);
                button.addEventListener('click', enrollCourse);
            }
        });
    }

    // Event listener برای تغییر دانشکده
    departmentSelect.addEventListener('change', function() {
        const departmentId = this.value;
        if (departmentId) {
            fetch(`/get-department-courses/?department_id=${departmentId}`)
                .then(response => response.json())
                .then(data => {
                    coursesTbody.innerHTML = '';
                    coursesTable.style.display = 'table';
                    
                    data.courses.forEach(course => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${course.code}</td>
                            <td>${course.name}</td>
                            <td>${course.credits}</td>
                            <td>${course.instructor__first_name} ${course.instructor__last_name}</td>
                            <td>${course.capacity}/${course.initial_capacity}</td>
                            <td>
                                <button class="btn btn-primary btn-sm" 
                                        data-course-id="${course.id}">
                                    انتخاب درس
                                </button>
                            </td>
                        `;
                        coursesTbody.appendChild(row);
                    });

                    // به‌روزرسانی وضعیت دکمه‌ها
                    loadEnrolledCourses();

                    // اضافه کردن event listeners
                    document.querySelectorAll('#courses-tbody [data-course-id]').forEach(button => {
                        button.addEventListener('click', enrollCourse);
                    });
                });
        } else {
            coursesTable.style.display = 'none';
        }
    });

    // تابع انتخاب درس - به‌روزشده
    function enrollCourse(e) {
        e.preventDefault();
        const courseId = this.dataset.courseId;
        
        fetch('/enroll-course/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `course_id=${courseId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showNotification(data.message, 'success');
                loadEnrolledCourses();
                loadDepartmentCourses(); // به‌روزرسانی لیست دروس و ظرفیت‌ها
            } else {
                showNotification(data.message, 'error');
            }
        })
        .catch(error => {
            showNotification('خطا در ثبت درس', 'error');
        });
    }

    // تابع حذف درس - به‌روزشده
    function dropCourse(e) {
        e.preventDefault();
        if (!confirm('آیا از حذف این درس اطمینان دارید؟')) {
            return;
        }

        const courseId = this.dataset.courseId;
        
        fetch('/drop-course/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `course_id=${courseId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showNotification(data.message, 'success');
                loadEnrolledCourses();
                loadDepartmentCourses(); // به‌روزرسانی لیست دروس و ظرفیت‌ها
            } else {
                showNotification(data.message, 'error');
            }
        })
        .catch(error => {
            showNotification('خطا در حذف درس', 'error');
        });
    }


    searchInput.addEventListener('input', function() {
        const searchValue = searchInput.value.trim().toLowerCase();

        document.querySelectorAll('#courses-tbody tr').forEach(row => {
            const courseCode = row.querySelector('td:nth-child(1)').textContent.trim().toLowerCase();
            const courseName = row.querySelector('td:nth-child(2)').textContent.trim().toLowerCase();

            if (courseCode.includes(searchValue) || courseName.includes(searchValue)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });

    // Event listener برای تغییر دانشکده
    departmentSelect.addEventListener('change', loadDepartmentCourses);

    function showNotification(message, type) {
        const notificationDiv = document.createElement('div');
        notificationDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} notification`;
        notificationDiv.style.position = 'fixed';
        notificationDiv.style.top = '20px';
        notificationDiv.style.right = '20px';
        notificationDiv.style.zIndex = '1000';
        notificationDiv.textContent = message;
        
        document.body.appendChild(notificationDiv);
        
        setTimeout(() => {
            notificationDiv.remove();
        }, 3000);
    }

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

    // فراخوانی اولیه دروس انتخاب شده
    loadEnrolledCourses();
});