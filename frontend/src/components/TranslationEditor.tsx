import { useState } from 'react';
import { Button } from '@/components/ui/button';
import type { Translation } from '@/types/api';
import { X, Save, CheckCircle } from 'lucide-react';

interface TranslationEditorProps {
  translation: Translation;
  onSave: (translationId: number, newText: string, isReviewed: boolean) => Promise<void>;
  onCancel: () => void;
}

export function TranslationEditor({ translation, onSave, onCancel }: TranslationEditorProps) {
  const [text, setText] = useState(translation.translation || '');
  const [isReviewed, setIsReviewed] = useState(translation.is_reviewed);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSave = async () => {
    setIsSaving(true);
    setError(null);

    try {
      await onSave(translation.translation_id, text, isReviewed);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save translation');
    } finally {
      setIsSaving(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onCancel();
    } else if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handleSave();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div
        className="bg-background max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-lg shadow-lg"
        onKeyDown={handleKeyPress}
      >
        <div className="flex items-center justify-between border-b p-6">
          <div>
            <h2 className="text-xl font-semibold">Edit Translation</h2>
            <p className="text-muted-foreground text-sm">
              Language: <span className="font-mono font-medium">{translation.language_iso}</span>
            </p>
          </div>
          <Button variant="ghost" size="sm" onClick={onCancel}>
            <X className="h-4 w-4" />
          </Button>
        </div>

        <div className="space-y-4 p-6">
          <div>
            <label htmlFor="translation-text" className="mb-2 block text-sm font-medium">
              Translation Text
            </label>
            <textarea
              id="translation-text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter translation..."
              rows={6}
              className="border-input focus:ring-ring focus:border-ring resize-vertical w-full rounded-md border px-3 py-2 shadow-sm focus:ring-2 focus:outline-none"
            />
            <p className="text-muted-foreground mt-1 text-xs">
              Word count: {text.trim().split(/\s+/).filter(Boolean).length}
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="is-reviewed"
              checked={isReviewed}
              onChange={(e) => setIsReviewed(e.target.checked)}
              className="border-input rounded"
            />
            <label
              htmlFor="is-reviewed"
              className="flex cursor-pointer items-center gap-1 text-sm font-medium"
            >
              <CheckCircle className="h-4 w-4" />
              Mark as reviewed
            </label>
          </div>

          {error && (
            <div className="border-destructive bg-destructive/10 rounded-lg border p-3">
              <p className="text-destructive text-sm">{error}</p>
            </div>
          )}

          <div className="bg-muted/50 rounded-lg p-4">
            <h3 className="mb-2 text-sm font-medium">Translation Details</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-muted-foreground">Translation ID:</span>
                <span className="ml-2 font-mono">{translation.translation_id}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Key ID:</span>
                <span className="ml-2 font-mono">{translation.key_id}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Modified By:</span>
                <span className="ml-2">{translation.modified_by_email}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Modified At:</span>
                <span className="ml-2">{translation.modified_at}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Current Status:</span>
                <span className="ml-2">
                  {translation.is_reviewed
                    ? 'Reviewed'
                    : translation.is_unverified
                      ? 'Unverified'
                      : 'Pending'}
                </span>
              </div>
              <div>
                <span className="text-muted-foreground">Words:</span>
                <span className="ml-2">{translation.words}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-muted/20 flex items-center justify-end gap-3 border-t p-6">
          <Button variant="outline" onClick={onCancel} disabled={isSaving}>
            Cancel
          </Button>
          <Button onClick={handleSave} disabled={isSaving}>
            {isSaving ? (
              <>
                <div className="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white"></div>
                Saving...
              </>
            ) : (
              <>
                <Save className="mr-2 h-4 w-4" />
                Save Translation
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}
