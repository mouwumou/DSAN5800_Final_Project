import axios from 'axios';

function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        headers: {
            authorization: `Bearer ${token}`
        }
    };
}

function handleError(err) {
    if (err.response) {
        // 服务器有返回响应，但状态码非2xx
        console.error(`服务器错误: 状态码=${err.response.status}`, err.response.data);
    } else if (err.request) {
        // 请求已发出，但未收到响应
        console.error('请求已发出但未收到响应: ', err.request);
    } else {
        // 在设置请求时发生错误
        console.error('请求设置错误: ', err.message);
    }
    // 根据需要，可以重新抛出错误或返回一个约定的错误对象
    throw err;
}

export async function getAllExpenses() {
    try {
        const response = await axios.get("/api/expense/expense/", getAuthHeaders());
        return response.data;
    } catch (err) {
        handleError(err);
    }
}

export async function createExpense(data) {
    try {
        const response = await axios.post("/api/expense/expense/", data, getAuthHeaders());
        return response.data;
    } catch (err) {
        handleError(err);
    }
}

export async function filterExpenseByCategory(category) {
    try {
        const response = await axios.get(`/api/expense/expense/filter_by_category?category=${encodeURIComponent(category)}`, getAuthHeaders());
        return response.data;
    } catch (err) {
        handleError(err);
    }
}

export async function filterExpenseByDateRange(start_date, end_date) {
    try {
        const response = await axios.get(`/api/expense/expense/filter_by_date_range?start_date=${encodeURIComponent(start_date)}&end_date=${encodeURIComponent(end_date)}`, getAuthHeaders());
        return response.data;
    } catch (err) {
        handleError(err);
    }
}
