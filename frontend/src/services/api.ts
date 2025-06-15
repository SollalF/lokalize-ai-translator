import type {
  TranslationKey,
  Translation,
  TranslationUpdate,
  TranslationRequest,
  TranslationResponse,
  BatchTranslationRequest,
  BatchTranslationResponse,
  SupportedLanguagesResponse,
  ProjectKeysParams,
  ProjectTranslationsParams,
  KeysCreateRequest,
  KeysCreateResponse,
  ProjectsListParams,
  ProjectsListResponse,
  GlossaryUploadParams,
  GlossaryUploadResponse,
  TranslationEvaluationRequest,
  TranslationEvaluationResponse,
} from '@/types/api';

const API_BASE = '/api/v1';

class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public response?: Response
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchApi<T>(url: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new ApiError(`HTTP error! status: ${response.status}`, response.status, response);
  }

  return response.json();
}

// Project Keys API
export async function getProjectKeys(params: ProjectKeysParams): Promise<TranslationKey[]> {
  const { project_id, ...queryParams } = params;
  const searchParams = new URLSearchParams();

  Object.entries(queryParams).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      searchParams.append(key, value.toString());
    }
  });

  const url = `${API_BASE}/projects/${project_id}/keys?${searchParams}`;
  return fetchApi<TranslationKey[]>(url);
}

// Project Translations API
export async function getProjectTranslations(
  params: ProjectTranslationsParams
): Promise<Translation[]> {
  const { project_id, ...queryParams } = params;
  const searchParams = new URLSearchParams();

  Object.entries(queryParams).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      searchParams.append(key, value.toString());
    }
  });

  const url = `${API_BASE}/projects/${project_id}/translations?${searchParams}`;
  return fetchApi<Translation[]>(url);
}

// Get specific translation
export async function getTranslation(
  projectId: string,
  translationId: number,
  disableReferences: 0 | 1 = 0
): Promise<Translation> {
  const url = `${API_BASE}/projects/${projectId}/translations/${translationId}?disable_references=${disableReferences}`;
  return fetchApi<Translation>(url);
}

// Update translation
export async function updateTranslation(
  projectId: string,
  translationId: number,
  updateData: TranslationUpdate
): Promise<Translation> {
  const url = `${API_BASE}/projects/${projectId}/translations/${translationId}`;
  return fetchApi<Translation>(url, {
    method: 'PUT',
    body: JSON.stringify(updateData),
  });
}

// Translation API
export async function translateText(request: TranslationRequest): Promise<TranslationResponse> {
  const url = `${API_BASE}/translation/translate/glossary`;
  return fetchApi<TranslationResponse>(url, {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function translateBatch(
  request: BatchTranslationRequest
): Promise<BatchTranslationResponse> {
  const url = `${API_BASE}/translation/translate/batch`;
  return fetchApi<BatchTranslationResponse>(url, {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function getSupportedLanguages(): Promise<SupportedLanguagesResponse> {
  const url = `${API_BASE}/translation/languages`;
  return fetchApi<SupportedLanguagesResponse>(url);
}

// Create keys
export async function createKeys(
  projectId: string,
  request: KeysCreateRequest
): Promise<KeysCreateResponse> {
  const url = `${API_BASE}/projects/${projectId}/keys`;
  return fetchApi<KeysCreateResponse>(url, {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// Get projects list
export async function getProjects(params: ProjectsListParams = {}): Promise<ProjectsListResponse> {
  const searchParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      searchParams.append(key, value.toString());
    }
  });

  const url = `${API_BASE}/projects${searchParams.toString() ? `?${searchParams}` : ''}`;
  return fetchApi<ProjectsListResponse>(url);
}

// Upload glossary file
export async function uploadGlossary(
  file: File,
  params: GlossaryUploadParams
): Promise<GlossaryUploadResponse> {
  const { project_id, source_language = 'en' } = params;

  const formData = new FormData();
  formData.append('file', file);

  const searchParams = new URLSearchParams({
    project_id,
    source_language,
  });

  const url = `${API_BASE}/glossary/load?${searchParams}`;

  const response = await fetch(url, {
    method: 'POST',
    body: formData,
    // Don't set Content-Type header - browser will set it with boundary for multipart/form-data
  });

  if (!response.ok) {
    throw new ApiError(`HTTP error! status: ${response.status}`, response.status, response);
  }

  return response.json();
}

// Evaluate translation
export async function evaluateTranslation(
  request: TranslationEvaluationRequest
): Promise<TranslationEvaluationResponse> {
  const url = `${API_BASE}/translation/evaluate`;
  return fetchApi<TranslationEvaluationResponse>(url, {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export { ApiError };
