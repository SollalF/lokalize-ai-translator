import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { uploadGlossary } from '@/services/api';
import type { GlossaryUploadResponse } from '@/types/api';
import { Upload, X, FileSpreadsheet, CheckCircle, AlertCircle } from 'lucide-react';

interface GlossaryUploaderProps {
  projectId: string;
  onClose: () => void;
  onSuccess?: (response: GlossaryUploadResponse) => void;
}

export function GlossaryUploader({ projectId, onClose, onSuccess }: GlossaryUploaderProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [sourceLanguage, setSourceLanguage] = useState('en');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<GlossaryUploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file type
      if (!file.name.toLowerCase().endsWith('.xlsx')) {
        setError('Please select an XLSX file.');
        return;
      }

      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB.');
        return;
      }

      setSelectedFile(file);
      setError(null);
      setUploadResult(null);
    }
  };

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault();
  };

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file) {
      // Handle file validation directly instead of creating synthetic event
      if (!file.name.toLowerCase().endsWith('.xlsx')) {
        setError('Please select an XLSX file.');
        return;
      }

      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB.');
        return;
      }

      setSelectedFile(file);
      setError(null);
      setUploadResult(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    setError(null);

    try {
      const response = await uploadGlossary(selectedFile, {
        project_id: projectId,
        source_language: sourceLanguage,
      });

      setUploadResult(response);
      onSuccess?.(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to upload glossary');
    } finally {
      setIsUploading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setUploadResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="bg-background max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-lg shadow-lg">
        <div className="flex items-center justify-between border-b p-6">
          <div>
            <h2 className="text-xl font-semibold">Upload Glossary File</h2>
            <p className="text-muted-foreground text-sm">
              Upload an XLSX file containing glossary terms for project:{' '}
              <span className="font-mono">{projectId}</span>
            </p>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>

        <div className="space-y-6 p-6">
          {/* Source Language Selection */}
          <div>
            <label htmlFor="source-language" className="mb-2 block text-sm font-medium">
              Source Language
            </label>
            <select
              id="source-language"
              value={sourceLanguage}
              onChange={(e) => setSourceLanguage(e.target.value)}
              className="border-input focus:ring-ring focus:border-ring w-full rounded-md border px-3 py-2 shadow-sm focus:ring-2 focus:outline-none"
            >
              <option value="en">English (en)</option>
              <option value="es">Spanish (es)</option>
              <option value="fr">French (fr)</option>
              <option value="de">German (de)</option>
              <option value="it">Italian (it)</option>
              <option value="pt">Portuguese (pt)</option>
              <option value="ru">Russian (ru)</option>
              <option value="zh">Chinese (zh)</option>
              <option value="ja">Japanese (ja)</option>
              <option value="ko">Korean (ko)</option>
            </select>
          </div>

          {/* File Upload Area */}
          <div>
            <label className="mb-2 block text-sm font-medium">Glossary File (XLSX)</label>
            <div
              className="border-input hover:bg-muted/50 cursor-pointer rounded-lg border-2 border-dashed p-6 text-center transition-colors"
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".xlsx"
                onChange={handleFileSelect}
                className="hidden"
              />

              {selectedFile ? (
                <div className="space-y-2">
                  <FileSpreadsheet className="text-primary mx-auto h-8 w-8" />
                  <div>
                    <p className="font-medium">{selectedFile.name}</p>
                    <p className="text-muted-foreground text-sm">
                      {formatFileSize(selectedFile.size)}
                    </p>
                  </div>
                  <Button variant="outline" size="sm" onClick={handleReset}>
                    Choose Different File
                  </Button>
                </div>
              ) : (
                <div className="space-y-2">
                  <Upload className="text-muted-foreground mx-auto h-8 w-8" />
                  <div>
                    <p className="font-medium">Click to upload or drag and drop</p>
                    <p className="text-muted-foreground text-sm">XLSX files only, max 10MB</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="border-destructive bg-destructive/10 flex items-center gap-2 rounded-lg border p-3">
              <AlertCircle className="text-destructive h-4 w-4" />
              <p className="text-destructive text-sm">{error}</p>
            </div>
          )}

          {/* Upload Result */}
          {uploadResult && (
            <div className="flex items-start gap-3 rounded-lg border border-green-200 bg-green-50 p-4">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <div className="flex-1">
                <h3 className="font-medium text-green-900">Upload Successful!</h3>
                <p className="text-sm text-green-700">{uploadResult.message}</p>

                <div className="mt-3 grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium text-green-800">Total Terms:</span>
                    <span className="ml-2 text-green-700">{uploadResult.stats.total_terms}</span>
                  </div>
                  <div>
                    <span className="font-medium text-green-800">Languages:</span>
                    <span className="ml-2 text-green-700">{uploadResult.stats.language_count}</span>
                  </div>
                  <div>
                    <span className="font-medium text-green-800">Case Sensitive:</span>
                    <span className="ml-2 text-green-700">
                      {uploadResult.stats.case_sensitive_terms}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-green-800">Case Insensitive:</span>
                    <span className="ml-2 text-green-700">
                      {uploadResult.stats.case_insensitive_terms}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-green-800">Forbidden Terms:</span>
                    <span className="ml-2 text-green-700">
                      {uploadResult.stats.forbidden_terms}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-green-800">Translatable Terms:</span>
                    <span className="ml-2 text-green-700">
                      {uploadResult.stats.translatable_terms}
                    </span>
                  </div>
                </div>

                {uploadResult.stats.available_languages.length > 0 && (
                  <div className="mt-3">
                    <span className="text-sm font-medium text-green-800">Available Languages:</span>
                    <div className="mt-1 flex flex-wrap gap-1">
                      {uploadResult.stats.available_languages.map((lang) => (
                        <span
                          key={lang}
                          className="rounded bg-green-100 px-2 py-1 text-xs font-medium text-green-800"
                        >
                          {lang}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="bg-muted/20 flex items-center justify-end gap-3 border-t p-6">
          <Button variant="outline" onClick={onClose} disabled={isUploading}>
            {uploadResult ? 'Close' : 'Cancel'}
          </Button>
          {!uploadResult && (
            <Button onClick={handleUpload} disabled={!selectedFile || isUploading}>
              {isUploading ? (
                <>
                  <div className="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white"></div>
                  Uploading...
                </>
              ) : (
                <>
                  <Upload className="mr-2 h-4 w-4" />
                  Upload Glossary
                </>
              )}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
