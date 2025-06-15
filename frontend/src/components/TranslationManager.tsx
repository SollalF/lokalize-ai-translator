import { useState } from 'react';
import { ProjectSelector } from '@/components/ProjectSelector';
import { TranslationList } from '@/components/TranslationList';
import { KeyCreator } from '@/components/KeyCreator';
import { GlossaryUploader } from '@/components/GlossaryUploader';
import { Button } from '@/components/ui/button';
import { getProjectTranslations } from '@/services/api';
import type { Translation, KeysCreateResponse, GlossaryUploadResponse } from '@/types/api';
import { Plus, Upload } from 'lucide-react';

export function TranslationManager() {
  const [projectId, setProjectId] = useState<string>('');
  const [translations, setTranslations] = useState<Translation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showKeyCreator, setShowKeyCreator] = useState(false);
  const [showGlossaryUploader, setShowGlossaryUploader] = useState(false);

  const handleProjectSelect = (selectedProjectId: string) => {
    setProjectId(selectedProjectId);
    setTranslations([]);
    setError(null);
  };

  const handleTranslationsLoad = (loadedTranslations: Translation[]) => {
    setTranslations(loadedTranslations);
  };

  const handleTranslationUpdate = (updatedTranslation: Translation) => {
    setTranslations((prev) =>
      prev.map((t) =>
        t.translation_id === updatedTranslation.translation_id ? updatedTranslation : t
      )
    );
  };

  const reloadTranslations = async () => {
    if (!projectId) return;

    setIsLoading(true);
    setError(null);

    try {
      const updatedTranslations = await getProjectTranslations({
        project_id: projectId,
        limit: 100,
        page: 1,
      });

      setTranslations(updatedTranslations);
    } catch (error) {
      console.error('Failed to reload translations:', error);
      setError(error instanceof Error ? error.message : 'Failed to reload translations');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeysCreated = async (response: KeysCreateResponse) => {
    // Show success message
    console.log(`Successfully created ${response.meta.created} keys`);

    // Automatically reload translations to show the new keys
    await reloadTranslations();
  };

  const handleGlossaryUploaded = (response: GlossaryUploadResponse) => {
    // Show success message
    console.log(`Successfully uploaded glossary with ${response.stats.total_terms} terms`);

    // You could potentially reload translations or show a success notification here
    // For now, we'll just log the success
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="mb-4 text-3xl font-bold">Lokalize AI Translator</h1>
        <p className="text-muted-foreground">
          Manage and translate your Lokalise project keys with AI assistance.
        </p>
      </div>

      <div className="space-y-6">
        <ProjectSelector
          projectId={projectId}
          onProjectSelect={handleProjectSelect}
          onTranslationsLoad={handleTranslationsLoad}
          onLoadingChange={setIsLoading}
          onError={setError}
        />

        {error && (
          <div className="border-destructive bg-destructive/10 rounded-lg border p-4">
            <p className="text-destructive">{error}</p>
          </div>
        )}

        {projectId && (
          <>
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">Project Actions</h2>
              <div className="flex gap-2">
                <Button variant="outline" onClick={() => setShowGlossaryUploader(true)}>
                  <Upload className="mr-2 h-4 w-4" />
                  Upload Glossary
                </Button>
                <Button onClick={() => setShowKeyCreator(true)}>
                  <Plus className="mr-2 h-4 w-4" />
                  Create New Keys
                </Button>
              </div>
            </div>

            <TranslationList
              translations={translations}
              projectId={projectId}
              isLoading={isLoading}
              onTranslationUpdate={handleTranslationUpdate}
            />
          </>
        )}

        {showKeyCreator && (
          <KeyCreator
            projectId={projectId}
            onKeysCreated={handleKeysCreated}
            onClose={() => setShowKeyCreator(false)}
          />
        )}

        {showGlossaryUploader && (
          <GlossaryUploader
            projectId={projectId}
            onSuccess={handleGlossaryUploaded}
            onClose={() => setShowGlossaryUploader(false)}
          />
        )}
      </div>
    </div>
  );
}
