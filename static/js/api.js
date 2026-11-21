/**
 * MediLink Enterprise — API Client Layer
 * Real REST API integration for all backend clinical modules.
 */

const API_BASE = '/api';

class ApiClient {
  constructor() {
    this.token = localStorage.getItem('medilink_token') || null;
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('medilink_token', token);
    } else {
      localStorage.removeItem('medilink_token');
    }
  }

  getToken() {
    return this.token;
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const headers = options.headers || {};

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    if (!(options.body instanceof FormData) && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }

    const config = {
      ...options,
      headers
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        let errData;
        try {
          errData = await response.json();
        } catch (e) {
          errData = { detail: response.statusText || 'Unknown Server Error' };
        }
        const error = new Error(errData.detail || `Request failed with status ${response.status}`);
        error.status = response.status;
        error.detail = errData.detail;
        throw error;
      }

      // Check if response is JSON
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }
      return await response.text();
    } catch (err) {
      console.error(`[API Error] ${options.method || 'GET'} ${endpoint}:`, err);
      throw err;
    }
  }

  // --- AUTH ---
  async login(username, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    if (data.access_token) {
      this.setToken(data.access_token);
    }
    return data;
  }

  async getMe() {
    return await this.request('/auth/me');
  }

  async getRoles() {
    return await this.request('/auth/roles');
  }

  async updateProfile(profileData) {
    return await this.request('/auth/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData)
    });
  }

  async changePassword(current_password, new_password) {
    return await this.request('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify({ current_password, new_password })
    });
  }

  async logout() {
    try {
      await this.request('/auth/logout', { method: 'POST' });
    } catch (e) {
      console.warn('Backend logout warning:', e);
    } finally {
      this.setToken(null);
    }
  }

  // --- PATIENTS ---
  async getPatients(search = '', limit = 100) {
    const q = search ? `?search=${encodeURIComponent(search)}&limit=${limit}` : `?limit=${limit}`;
    return await this.request(`/patients${q}`);
  }

  async getPatient(aadhaar) {
    return await this.request(`/patients/${encodeURIComponent(aadhaar)}`);
  }

  async registerPatient(patientData) {
    return await this.request('/patients', {
      method: 'POST',
      body: JSON.stringify(patientData)
    });
  }

  async updatePatient(aadhaar, patientData) {
    return await this.request(`/patients/${encodeURIComponent(aadhaar)}`, {
      method: 'PUT',
      body: JSON.stringify(patientData)
    });
  }

  async triggerBreakGlass(aadhaar, reason) {
    return await this.request(`/patients/${encodeURIComponent(aadhaar)}/break-glass?reason=${encodeURIComponent(reason)}`, {
      method: 'POST'
    });
  }

  // --- MEDICAL RECORDS ---
  async getRecords(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return await this.request(`/records${qs ? '?' + qs : ''}`);
  }

  async getRecord(recordId) {
    return await this.request(`/records/${recordId}`);
  }

  async createRecord(recordData) {
    return await this.request('/records', {
      method: 'POST',
      body: JSON.stringify(recordData)
    });
  }

  // --- LAB REPORTS ---
  async getLabs(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return await this.request(`/labs${qs ? '?' + qs : ''}`);
  }

  async addLabReport(labData) {
    return await this.request('/labs', {
      method: 'POST',
      body: JSON.stringify(labData)
    });
  }

  async uploadLabPdf(formData) {
    return await this.request('/labs/upload', {
      method: 'POST',
      body: formData
    });
  }

  getLabDownloadUrl(reportId) {
    return `${API_BASE}/labs/${reportId}/download`;
  }

  // --- BEDS & WARDS ---
  async getBeds(hospitalId = null, ward = 'ALL', status = 'ALL') {
    const params = {};
    if (hospitalId) params.hospital_id = hospitalId;
    if (ward && ward !== 'ALL') params.ward = ward;
    if (status && status !== 'ALL') params.status_filter = status;
    const qs = new URLSearchParams(params).toString();
    return await this.request(`/beds${qs ? '?' + qs : ''}`);
  }

  async admitBed(admitData) {
    return await this.request('/beds/admit', {
      method: 'POST',
      body: JSON.stringify(admitData)
    });
  }

  async dischargeBed(allocationId) {
    return await this.request(`/beds/${allocationId}/discharge`, {
      method: 'POST'
    });
  }

  async cleanBed(allocationId) {
    return await this.request(`/beds/${allocationId}/clean`, {
      method: 'POST'
    });
  }

  // --- OPD QUEUE ---
  async getQueue(hospitalId = null, doctorId = null, status = 'ALL') {
    const params = {};
    if (hospitalId) params.hospital_id = hospitalId;
    if (doctorId) params.doctor_id = doctorId;
    if (status && status !== 'ALL') params.status_filter = status;
    const qs = new URLSearchParams(params).toString();
    return await this.request(`/queue${qs ? '?' + qs : ''}`);
  }

  async issueQueueToken(issueData) {
    return await this.request('/queue/issue', {
      method: 'POST',
      body: JSON.stringify(issueData)
    });
  }

  async updateQueueStatus(queueId, status) {
    return await this.request(`/queue/${queueId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status })
    });
  }

  // --- APPOINTMENTS ---
  async getAppointments(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return await this.request(`/appointments${qs ? '?' + qs : ''}`);
  }

  async bookAppointment(data) {
    return await this.request('/appointments', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async rescheduleAppointment(appointmentId, data) {
    return await this.request(`/appointments/${appointmentId}/reschedule`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async updateAppointmentStatus(appointmentId, status) {
    return await this.request(`/appointments/${appointmentId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status })
    });
  }

  // --- HOSPITALS & DOCTORS ---
  async getHospitals() {
    return await this.request('/hospitals');
  }

  async getDoctors() {
    return await this.request('/doctors');
  }

  // --- ANALYTICS ---
  async getDashboardStats(hospitalId = null) {
    const q = hospitalId ? `?hospital_id=${hospitalId}` : '';
    return await this.request(`/analytics/dashboard${q}`);
  }

  async getDepartmentVolume() {
    return await this.request('/analytics/department-volume');
  }

  async getHospitalVolume() {
    return await this.request('/analytics/hospital-volume');
  }

  getCsvReportUrl(reportType = 'records', hospitalId = null) {
    const q = hospitalId ? `&hospital_id=${hospitalId}` : '';
    return `${API_BASE}/analytics/reports/csv?report_type=${reportType}${q}`;
  }

  // --- AUDIT LOGS ---
  async getAuditLogs(aadhaar = '', limit = 50) {
    const params = { limit };
    if (aadhaar) params.aadhaar = aadhaar;
    const qs = new URLSearchParams(params).toString();
    return await this.request(`/audit?${qs}`);
  }

  // --- SQL WORKBENCH ---
  async getSqlQueries() {
    return await this.request('/sql/queries');
  }

  async executeSqlQuery(queryKey, param = '') {
    return await this.request('/sql/execute', {
      method: 'POST',
      body: JSON.stringify({ query_key: queryKey, param })
    });
  }

  // --- NOTIFICATIONS ---
  async getNotifications() {
    return await this.request('/notifications');
  }

  async markNotificationRead(id) {
    return await this.request(`/notifications/${id}/read`, { method: 'PUT' });
  }

  async markAllNotificationsRead() {
    return await this.request('/notifications/mark-all-read', { method: 'PUT' });
  }

  // --- BACKUP & RESTORE ---
  async exportBackup() {
    return await this.request('/backup/export');
  }

  async importBackup(jsonData) {
    return await this.request('/backup/import', {
      method: 'POST',
      body: JSON.stringify(jsonData)
    });
  }

  // --- HEALTH ---
  async checkHealth() {
    return await this.request('/health');
  }
}

window.api = new ApiClient();
