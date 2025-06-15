export interface TranslationKey {
  key_id: number;
  key_name: string | PlatformKeyNames;
  source_text: string;
  translated_text: string | null;
  is_translated: boolean;
  language_code: string;
  created_at: string;
  created_at_timestamp: number;
  description: string;
  platforms: string[];
  tags: string[];
  is_plural: boolean;
  plural_name: string;
  is_hidden: boolean;
  is_archived: boolean;
  context: string;
  base_words: number;
  char_limit: number;
  translation_metadata: TranslationMetadata | null;
  modified_at: string;
  modified_at_timestamp: number;
  translations_modified_at: string;
  translations_modified_at_timestamp: number;
}

export interface PlatformKeyNames {
  ios: string;
  android: string;
  web: string;
  other: string;
}

export interface TranslationMetadata {
  translation_id: number;
  modified_by: number;
  modified_by_email: string;
  modified_at: string;
  modified_at_timestamp: number;
  is_reviewed: boolean;
  is_unverified: boolean;
  reviewed_by: number;
  words: number;
}

export interface Translation {
  translation_id: number;
  key_id: number;
  language_iso: string;
  translation: string;
  modified_at: string;
  modified_at_timestamp: number;
  modified_by: number;
  modified_by_email: string;
  is_unverified: boolean;
  is_reviewed: boolean;
  reviewed_by: number;
  words: number;
  custom_translation_statuses: string[];
  task_id: number | null;
  segment_number: number;
}

export interface TranslationUpdate {
  translation: string;
  is_unverified?: boolean;
  is_reviewed?: boolean;
}

export interface TranslationRequest {
  source_text: string;
  source_lang: string;
  target_lang: string;
  project_id: string;
  preserve_forbidden_terms?: boolean;
  translate_allowed_terms?: boolean;
}

// Note: GlossaryTerm interface is defined below with translation evaluation types

export interface VerificationResults {
  success: boolean;
  missing_terms: GlossaryTerm[];
  warnings: string[];
  suggestions: string[];
  found_wrapped_terms: Record<string, string>;
  cleaned_text: string;
}

export interface TranslationResponse {
  translated_text: string;
  source_text: string;
  source_lang: string;
  target_lang: string;
  glossary_terms_found: GlossaryTerm[];
  wrapped_text: string;
  verification_results: VerificationResults;
}

export interface BatchTranslationRequest {
  texts: string[];
  source_lang: string;
  target_lang: string;
}

export interface BatchTranslationResponse {
  translations: TranslationResponse[];
}

export interface SupportedLanguagesResponse {
  languages: Record<string, string>;
}

export interface ProjectKeysParams {
  project_id: string;
  include_translations?: 0 | 1;
  include_comments?: 0 | 1;
  include_screenshots?: 0 | 1;
  filter_translation_lang_ids?: string;
  filter_tags?: string;
  filter_platforms?: string;
  filter_untranslated?: 0 | 1;
  filter_archived?: 'include' | 'exclude' | 'only';
  filter_keys?: string;
  filter_key_ids?: string;
  limit?: number;
  page?: number;
  reviewed_only?: boolean;
}

export interface ProjectTranslationsParams {
  project_id: string;
  disable_references?: 0 | 1;
  filter_lang_id?: number;
  filter_is_reviewed?: 0 | 1;
  filter_unverified?: 0 | 1;
  filter_untranslated?: 0 | 1;
  filter_qa_issues?: string;
  filter_active_task_id?: number;
  pagination?: 'offset' | 'cursor';
  limit?: number;
  page?: number;
  cursor?: string;
}

// Key Creation Types
export interface KeyFilenames {
  ios?: string;
  android?: string;
  web?: string;
  other?: string;
}

export interface KeyComment {
  comment: string;
}

export interface KeyScreenshot {
  data: string; // Base64 encoded image data
  title?: string;
  description?: string;
  screenshot_tags?: string[];
}

export interface KeyTranslation {
  language_iso: string;
  translation: string | Record<string, string>; // Can be string or object for plurals
  is_reviewed?: boolean;
  is_unverified?: boolean;
  custom_translation_status_ids?: number[];
}

export interface KeyCreate {
  key_name: string;
  platforms: string[];
  description?: string;
  filenames?: KeyFilenames;
  tags?: string[];
  comments?: KeyComment[];
  screenshots?: KeyScreenshot[];
  translations?: KeyTranslation[];
  is_plural?: boolean;
  plural_name?: string;
  is_hidden?: boolean;
  is_archived?: boolean;
  context?: string;
  char_limit?: number;
  custom_attributes?: string; // JSON string
}

export interface KeysCreateRequest {
  keys: KeyCreate[];
  use_automations?: boolean;
}

export interface KeyCreateMeta {
  count: number;
  created: number;
  limit: number | null;
  errors: Record<string, unknown>;
}

export interface KeysCreateResponse {
  data: TranslationKey[];
  meta: KeyCreateMeta;
}

// Projects API Types
export interface ProjectSettings {
  per_platform_key_names: boolean;
  reviewing: boolean;
  auto_toggle_unverified: boolean;
  offline_translation: boolean;
  key_editing: boolean;
  inline_machine_translations: boolean;
  branching: boolean;
  segmentation: boolean;
  custom_translation_statuses: boolean;
  custom_translation_statuses_allow_multiple: boolean;
  contributor_preview_download_enabled: boolean;
}

export interface ProjectQAIssues {
  not_reviewed: number;
  unverified: number;
  spelling_grammar: number;
  inconsistent_placeholders: number;
  inconsistent_html: number;
  different_number_of_urls: number;
  different_urls: number;
  leading_whitespace: number;
  trailing_whitespace: number;
  different_number_of_email_address: number;
  different_email_address: number;
  different_brackets: number;
  different_numbers: number;
  double_space: number;
  special_placeholder: number;
  unbalanced_brackets: number;
}

export interface ProjectStatistics {
  progress_total: number;
  keys_total: number;
  team: number;
  base_words: number;
  qa_issues_total: number;
  qa_issues: ProjectQAIssues;
}

export interface ProjectLanguage {
  language_id: number;
  language_iso: string;
  progress: number;
  words_to_do: number;
}

export interface Project {
  project_id: string;
  project_type: string;
  name: string;
  description: string;
  created_at: string;
  created_at_timestamp: number;
  created_by: number;
  created_by_email: string;
  team_id: number;
  base_language_id: number;
  base_language_iso: string;
  settings?: ProjectSettings;
  statistics?: ProjectStatistics;
  languages: ProjectLanguage[];
}

export interface ProjectsListParams {
  filter_team_id?: number;
  filter_names?: string;
  include_statistics?: 0 | 1;
  include_settings?: 0 | 1;
  limit?: number;
  page?: number;
}

export interface ProjectsListResponse {
  projects: Project[];
  total_count: number;
}

// Glossary Upload Types
export interface GlossaryUploadStats {
  total_terms: number;
  case_sensitive_terms: number;
  case_insensitive_terms: number;
  forbidden_terms: number;
  translatable_terms: number;
  available_languages: string[];
  language_count: number;
}

export interface GlossaryUploadResponse {
  success: boolean;
  message: string;
  stats: GlossaryUploadStats;
}

export interface GlossaryUploadParams {
  project_id: string;
  source_language?: string;
}

// Translation Evaluation Types
export interface TranslationEvaluationRequest {
  source_text: string;
  source_lang: string;
  translated_text: string;
  target_lang: string;
  project_id: string;
}

export interface MetricScores {
  bleu: number | null;
  ter: number | null;
  chrf: number | null;
  edit_distance: number | null;
}

export interface GlossaryTerm {
  term: string;
  matched_text: string;
  start: number;
  end: number;
  case_sensitive: boolean;
  forbidden: boolean;
  translatable: boolean;
  translations: Record<string, string>;
}

export interface GlossaryCompliance {
  terms_found_in_source: GlossaryTerm[];
  terms_correctly_handled: GlossaryTerm[];
  terms_incorrectly_handled: GlossaryTerm[];
  compliance_score: number;
  compliance_summary: string;
}

export interface SpecificComment {
  part: string;
  comment: string;
}

export interface LLMFeedback {
  strengths: string[];
  weaknesses: string[];
  specific_comments: SpecificComment[];
  suggestions: string[];
  summary: string;
}

export interface TranslationEvaluationResponse {
  source_text: string;
  translated_text: string;
  reference_text: string | null;
  source_lang: string;
  target_lang: string;
  metric_scores: MetricScores;
  glossary_compliance: GlossaryCompliance;
  llm_feedback: LLMFeedback;
  overall_assessment: string;
}
