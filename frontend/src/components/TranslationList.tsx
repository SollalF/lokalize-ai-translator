import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { TranslationEditor } from '@/components/TranslationEditor';
import { TranslationEvaluationModal } from '@/components/TranslationEvaluationModal';
import { updateTranslation, translateText } from '@/services/api';
import type { Translation } from '@/types/api';
import {
  CheckCircle,
  Clock,
  AlertCircle,
  Pencil,
  Sparkles,
  Zap,
  MessageSquare,
} from 'lucide-react';

interface TranslationListProps {
  translations: Translation[];
  projectId: string;
  isLoading: boolean;
  onTranslationUpdate: (translation: Translation) => void;
}

export function TranslationList({
  translations,
  projectId,
  isLoading,
  onTranslationUpdate,
}: TranslationListProps) {
  const [editingTranslation, setEditingTranslation] = useState<Translation | null>(null);
  const [evaluatingTranslation, setEvaluatingTranslation] = useState<{
    translation: Translation;
    sourceText: string;
  } | null>(null);
  const [isTranslating, setIsTranslating] = useState<number | null>(null);
  const [isBulkTranslating, setIsBulkTranslating] = useState(false);
  const [bulkProgress, setBulkProgress] = useState({ current: 0, total: 0 });

  const handleEdit = (translation: Translation) => {
    setEditingTranslation(translation);
  };

  const handleSave = async (translationId: number, newText: string, isReviewed: boolean) => {
    try {
      const updatedTranslation = await updateTranslation(projectId, translationId, {
        translation: newText,
        is_reviewed: isReviewed,
      });
      onTranslationUpdate(updatedTranslation);
      setEditingTranslation(null);
    } catch (error) {
      console.error('Failed to update translation:', error);
      throw error;
    }
  };

  const handleCancel = () => {
    setEditingTranslation(null);
  };

  const handleEvaluate = (translation: Translation) => {
    // Find the English source text for this key
    const englishTranslation = translations.find(
      (t) =>
        t.key_id === translation.key_id && (t.language_iso === 'en' || t.language_iso === 'en_US')
    );

    if (!englishTranslation?.translation) {
      console.error('No English source text found for evaluation');
      return;
    }

    setEvaluatingTranslation({
      translation,
      sourceText: englishTranslation.translation,
    });
  };

  const handleAutoTranslate = async (translation: Translation) => {
    setIsTranslating(translation.translation_id);
    try {
      // For auto-translation, we'll use the source text from the first English translation
      const englishTranslation = translations.find(
        (t) =>
          t.key_id === translation.key_id && (t.language_iso === 'en' || t.language_iso === 'en_US')
      );

      if (!englishTranslation?.translation) {
        throw new Error('No source text found for translation');
      }

      const result = await translateText({
        source_text: englishTranslation.translation,
        source_lang: 'en',
        target_lang: translation.language_iso.split('_')[0], // Get base language code
        project_id: projectId,
        preserve_forbidden_terms: true,
        translate_allowed_terms: true,
      });

      const updatedTranslation = await updateTranslation(projectId, translation.translation_id, {
        translation: result.translated_text,
        is_reviewed: false,
      });

      onTranslationUpdate(updatedTranslation);
    } catch (error) {
      console.error('Failed to auto-translate:', error);
    } finally {
      setIsTranslating(null);
    }
  };

  const handleBulkAutoTranslate = async () => {
    // Find all translations that are missing or empty
    const missingTranslations = translations.filter(
      (t) => !t.translation || t.translation.trim() === ''
    );

    if (missingTranslations.length === 0) {
      return;
    }

    setIsBulkTranslating(true);
    setBulkProgress({ current: 0, total: missingTranslations.length });

    let successCount = 0;
    let failureCount = 0;

    for (let i = 0; i < missingTranslations.length; i++) {
      const translation = missingTranslations[i];
      setBulkProgress({ current: i + 1, total: missingTranslations.length });

      try {
        // Find the English source text for this key
        const englishTranslation = translations.find(
          (t) =>
            t.key_id === translation.key_id &&
            (t.language_iso === 'en' || t.language_iso === 'en_US')
        );

        if (!englishTranslation?.translation) {
          console.warn(`No source text found for translation ${translation.translation_id}`);
          failureCount++;
          continue;
        }

        const result = await translateText({
          source_text: englishTranslation.translation,
          source_lang: 'en',
          target_lang: translation.language_iso.split('_')[0], // Get base language code
          project_id: projectId,
          preserve_forbidden_terms: true,
          translate_allowed_terms: true,
        });

        const updatedTranslation = await updateTranslation(projectId, translation.translation_id, {
          translation: result.translated_text,
          is_reviewed: false,
        });

        onTranslationUpdate(updatedTranslation);
        successCount++;

        // Add a small delay to avoid overwhelming the API
        await new Promise((resolve) => setTimeout(resolve, 500));
      } catch (error) {
        console.error(`Failed to auto-translate ${translation.translation_id}:`, error);
        failureCount++;
      }
    }

    console.log(
      `Bulk auto-translate completed: ${successCount} successful, ${failureCount} failed`
    );

    setIsBulkTranslating(false);
    setBulkProgress({ current: 0, total: 0 });
  };

  const getStatusIcon = (translation: Translation) => {
    if (translation.is_reviewed) {
      return <CheckCircle className="h-4 w-4 text-green-600" />;
    }
    if (translation.is_unverified) {
      return <AlertCircle className="h-4 w-4 text-yellow-600" />;
    }
    return <Clock className="h-4 w-4 text-gray-400" />;
  };

  const getStatusText = (translation: Translation) => {
    if (translation.is_reviewed) return 'Reviewed';
    if (translation.is_unverified) return 'Unverified';
    return 'Pending';
  };

  // Group translations by key_id for better organization
  const groupedTranslations = translations.reduce(
    (acc, translation) => {
      if (!acc[translation.key_id]) {
        acc[translation.key_id] = [];
      }
      acc[translation.key_id].push(translation);
      return acc;
    },
    {} as Record<number, Translation[]>
  );

  if (isLoading) {
    return (
      <div className="rounded-lg border p-6 shadow-sm">
        <div className="flex items-center justify-center py-8">
          <div className="border-primary h-8 w-8 animate-spin rounded-full border-b-2"></div>
          <span className="ml-2">Loading translations...</span>
        </div>
      </div>
    );
  }

  if (translations.length === 0) {
    return (
      <div className="rounded-lg border p-6 shadow-sm">
        <p className="text-muted-foreground py-8 text-center">
          No translations found. Try loading a project first.
        </p>
      </div>
    );
  }

  // Calculate how many translations are missing
  const missingTranslations = translations.filter(
    (t) => !t.translation || t.translation.trim() === ''
  );

  return (
    <div className="space-y-6">
      <div className="rounded-lg border p-6 shadow-sm">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold">Translations ({translations.length} items)</h2>
          {missingTranslations.length > 0 && (
            <div className="flex items-center gap-4">
              {isBulkTranslating && (
                <div className="text-muted-foreground flex items-center gap-2 text-sm">
                  <div className="border-primary h-4 w-4 animate-spin rounded-full border-b-2"></div>
                  <span>
                    Translating {bulkProgress.current} of {bulkProgress.total}...
                  </span>
                </div>
              )}
              <Button
                onClick={handleBulkAutoTranslate}
                disabled={isBulkTranslating}
                variant="outline"
                size="sm"
              >
                {isBulkTranslating ? (
                  <>
                    <div className="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-current"></div>
                    Translating...
                  </>
                ) : (
                  <>
                    <Zap className="mr-2 h-4 w-4" />
                    Auto-translate All Missing ({missingTranslations.length})
                  </>
                )}
              </Button>
            </div>
          )}
        </div>

        <div className="space-y-6">
          {Object.entries(groupedTranslations).map(([keyId, keyTranslations]) => (
            <div key={keyId} className="rounded-lg border p-4">
              <div className="mb-4">
                <h3 className="text-lg font-medium">Key ID: {keyId}</h3>
                <p className="text-muted-foreground text-sm">
                  {keyTranslations.length} language(s)
                </p>
              </div>

              <div className="space-y-3">
                {keyTranslations.map((translation) => (
                  <div
                    key={translation.translation_id}
                    className="bg-muted/50 flex items-center justify-between rounded-md p-3"
                  >
                    <div className="min-w-0 flex-1">
                      <div className="mb-1 flex items-center gap-2">
                        <span className="font-mono text-sm font-medium">
                          {translation.language_iso}
                        </span>
                        {getStatusIcon(translation)}
                        <span className="text-muted-foreground text-sm">
                          {getStatusText(translation)}
                        </span>
                      </div>
                      <p className="text-sm break-words">
                        {translation.translation || (
                          <span className="text-muted-foreground italic">No translation</span>
                        )}
                      </p>
                    </div>

                    <div className="ml-4 flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleAutoTranslate(translation)}
                        disabled={isTranslating === translation.translation_id || isBulkTranslating}
                      >
                        {isTranslating === translation.translation_id ? (
                          <div className="border-primary h-4 w-4 animate-spin rounded-full border-b-2"></div>
                        ) : (
                          <Sparkles className="h-4 w-4" />
                        )}
                        Auto-translate
                      </Button>
                      {translation.translation && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleEvaluate(translation)}
                          disabled={isBulkTranslating}
                        >
                          <MessageSquare className="h-4 w-4" />
                          Get Feedback
                        </Button>
                      )}
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleEdit(translation)}
                        disabled={isBulkTranslating}
                      >
                        <Pencil className="h-4 w-4" />
                        Edit
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {editingTranslation && (
        <TranslationEditor
          translation={editingTranslation}
          onSave={handleSave}
          onCancel={handleCancel}
        />
      )}

      {evaluatingTranslation && (
        <TranslationEvaluationModal
          translation={evaluatingTranslation.translation}
          sourceText={evaluatingTranslation.sourceText}
          projectId={projectId}
          onClose={() => setEvaluatingTranslation(null)}
        />
      )}
    </div>
  );
}
