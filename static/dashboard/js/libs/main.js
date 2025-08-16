export function stickyFn(){
    console.log("Dashboard Initialized");
}


import axios from "axios";

export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Create axios instance
const axiosInstance = axios.create({
  baseURL: "/",
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": getCookie("csrftoken"),
  },
  withCredentials: true,
});
export default axiosInstance;


export function getCsrfToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]")?.value;
}