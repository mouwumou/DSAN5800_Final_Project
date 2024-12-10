import axios from 'axios';

export async function login(loginInfo) {
    try {
      const resp = await axios.post("/api/user/token/", loginInfo);
      return resp;
    } catch (err) {
      if (err.response && err.response.status === 401) {
        return false;
      }
      // 如果不是401，则可以选择抛出错误，让上层统一处理
      throw err;
    }
  }
  

export async function whoAmI() {
    // get http://study.yuanjin.tech/api/user/whoami
    // authorization: bearer toeknxxxxx
    var token = localStorage.getItem("token");
    if (!token) {
        return null;
    };
    var resp = await axios.get("/api/user/user/user_detail/", {
        headers: {
            authorization: `Bearer ${token}`
        }
    }).catch((err) => {
        if (err.response.status == 401) {
            localStorage.removeItem("token")
        }
    })
    return resp;
}

export function logOut() {
    localStorage.removeItem("token");
}

export async function changePassword(payload) {
    var token = localStorage.getItem("token");
    if (!token) {
        return null;
    };
    var resp = await axios.post("/api/user/user/change_password/", payload, {
        headers: {
            authorization: `Bearer ${token}`
        }
    });
    return resp;
}

export async function getDepartments() {
    var token = localStorage.getItem("token");
    if (!token) {
        return null;
    };
    var resp = await axios.get("/api/user/department/", {
        headers: {
            authorization: `Bearer ${token}`
        }
    });
    return resp;
}

export async function getSystemSet() {
    var resp = await axios.get("/api/exam/system-set/1/");
    return resp;
}

export async function update_system_title(params) {
    var token = localStorage.getItem("token");
    if (!token) {
        return null;
    }
    var resp = await axios.post("/api/exam/system-set/change_title/", params, {
        headers: {
            authorization: `Bearer ${token}`
        }
    });
    return resp;
}
