import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (userData) => api.post("/auth/register", userData),
  login: (credentials) => api.post("/auth/login", credentials),
};

export const chatAPI = {
  sendMessage: (message) => api.post("/agent/chat", message),
  getConversationHistory: (conversationId = null) =>
    api.get(
      `/agent/conversation/history${
        conversationId ? `?conversation_id=${conversationId}` : ""
      }`
    ),
  clearConversation: () => api.delete("/agent/conversation/clear"),
};

export const userAPI = {
  getCurrentUser: () => api.get("/users/me"),
};

export default api;
