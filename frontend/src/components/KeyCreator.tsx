import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { createKeys } from '@/services/api';
import type { KeyCreate, KeysCreateResponse } from '@/types/api';
import { Plus, X, Save } from 'lucide-react';

interface KeyCreatorProps {
  projectId: string;
  onKeysCreated: (response: KeysCreateResponse) => void;
  onClose: () => void;
}

export function KeyCreator({ projectId, onKeysCreated, onClose }: KeyCreatorProps) {
  const [keys, setKeys] = useState<KeyCreate[]>([
    {
      key_name: '',
      platforms: ['web'],
      description: '',
      tags: [],
      translations: [
        {
          language_iso: 'en',
          translation: '',
          is_reviewed: false,
        },
      ],
      is_plural: false,
      is_hidden: false,
      is_archived: false,
      context: '',
    },
  ]);
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const addKey = () => {
    setKeys([
      ...keys,
      {
        key_name: '',
        platforms: ['web'],
        description: '',
        tags: [],
        translations: [
          {
            language_iso: 'en',
            translation: '',
            is_reviewed: false,
          },
        ],
        is_plural: false,
        is_hidden: false,
        is_archived: false,
        context: '',
      },
    ]);
  };

  const removeKey = (index: number) => {
    if (keys.length > 1) {
      setKeys(keys.filter((_, i) => i !== index));
    }
  };

  const updateKey = (index: number, field: keyof KeyCreate, value: unknown) => {
    const updatedKeys = [...keys];
    updatedKeys[index] = { ...updatedKeys[index], [field]: value };
    setKeys(updatedKeys);
  };

  const updateTranslation = (
    keyIndex: number,
    translationIndex: number,
    field: string,
    value: unknown
  ) => {
    const updatedKeys = [...keys];
    const translations = [...(updatedKeys[keyIndex].translations || [])];
    translations[translationIndex] = { ...translations[translationIndex], [field]: value };
    updatedKeys[keyIndex] = { ...updatedKeys[keyIndex], translations };
    setKeys(updatedKeys);
  };

  const handleSubmit = async () => {
    setIsCreating(true);
    setError(null);

    try {
      const validKeys = keys.filter(
        (key) =>
          key.key_name.trim() &&
          key.translations?.some((t) => {
            const translation = t.translation;
            return typeof translation === 'string'
              ? translation.trim()
              : Object.values(translation).some((v) => v.trim());
          })
      );

      if (validKeys.length === 0) {
        throw new Error('Please provide at least one key with a name and translation');
      }

      const response = await createKeys(projectId, {
        keys: validKeys,
        use_automations: false,
      });

      onKeysCreated(response);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create keys');
    } finally {
      setIsCreating(false);
    }
  };

  const availablePlatforms = ['ios', 'android', 'web', 'other'];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="bg-background max-h-[90vh] w-full max-w-4xl overflow-y-auto rounded-lg shadow-lg">
        <div className="flex items-center justify-between border-b p-6">
          <div>
            <h2 className="text-xl font-semibold">Create New Keys</h2>
            <p className="text-muted-foreground text-sm">
              Add new translation keys to project: <span className="font-mono">{projectId}</span>
            </p>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>

        <div className="space-y-6 p-6">
          {keys.map((key, keyIndex) => (
            <div key={keyIndex} className="rounded-lg border p-4">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="font-medium">Key {keyIndex + 1}</h3>
                {keys.length > 1 && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeKey(keyIndex)}
                    className="text-red-600 hover:text-red-700"
                  >
                    <X className="h-4 w-4" />
                    Remove
                  </Button>
                )}
              </div>

              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm font-medium">Key Name *</label>
                  <input
                    type="text"
                    value={key.key_name}
                    onChange={(e) => updateKey(keyIndex, 'key_name', e.target.value)}
                    placeholder="e.g., welcome_message"
                    className="border-input focus:ring-ring focus:border-ring w-full rounded-md border px-3 py-2 shadow-sm focus:ring-2 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium">Description</label>
                  <input
                    type="text"
                    value={key.description || ''}
                    onChange={(e) => updateKey(keyIndex, 'description', e.target.value)}
                    placeholder="Description of this key"
                    className="border-input focus:ring-ring focus:border-ring w-full rounded-md border px-3 py-2 shadow-sm focus:ring-2 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium">Platforms</label>
                  <div className="flex flex-wrap gap-2">
                    {availablePlatforms.map((platform) => (
                      <label key={platform} className="flex cursor-pointer items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={key.platforms.includes(platform)}
                          onChange={(e) => {
                            const platforms = e.target.checked
                              ? [...key.platforms, platform]
                              : key.platforms.filter((p) => p !== platform);
                            updateKey(keyIndex, 'platforms', platforms);
                          }}
                          className="border-input rounded"
                        />
                        <span className="text-sm capitalize">{platform}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium">Tags (comma-separated)</label>
                  <input
                    type="text"
                    value={key.tags?.join(', ') || ''}
                    onChange={(e) =>
                      updateKey(
                        keyIndex,
                        'tags',
                        e.target.value
                          .split(',')
                          .map((tag) => tag.trim())
                          .filter(Boolean)
                      )
                    }
                    placeholder="ui, button, navigation"
                    className="border-input focus:ring-ring focus:border-ring w-full rounded-md border px-3 py-2 shadow-sm focus:ring-2 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium">Context</label>
                  <input
                    type="text"
                    value={key.context || ''}
                    onChange={(e) => updateKey(keyIndex, 'context', e.target.value)}
                    placeholder="Where this key is used"
                    className="border-input focus:ring-ring focus:border-ring w-full rounded-md border px-3 py-2 shadow-sm focus:ring-2 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm font-medium">Character Limit</label>
                  <input
                    type="number"
                    value={key.char_limit || ''}
                    onChange={(e) =>
                      updateKey(
                        keyIndex,
                        'char_limit',
                        e.target.value ? parseInt(e.target.value) : undefined
                      )
                    }
                    placeholder="Optional character limit"
                    className="border-input focus:ring-ring focus:border-ring w-full rounded-md border px-3 py-2 shadow-sm focus:ring-2 focus:outline-none"
                  />
                </div>
              </div>

              <div className="mt-4">
                <label className="mb-2 block text-sm font-medium">English Translation *</label>
                <textarea
                  value={(key.translations?.[0]?.translation as string) || ''}
                  onChange={(e) => updateTranslation(keyIndex, 0, 'translation', e.target.value)}
                  placeholder="Enter the English text for this key"
                  rows={3}
                  className="border-input focus:ring-ring focus:border-ring w-full rounded-md border px-3 py-2 shadow-sm focus:ring-2 focus:outline-none"
                />
              </div>
            </div>
          ))}

          <Button onClick={addKey} variant="outline" className="w-full">
            <Plus className="mr-2 h-4 w-4" />
            Add Another Key
          </Button>

          {error && (
            <div className="border-destructive bg-destructive/10 rounded-lg border p-3">
              <p className="text-destructive text-sm">{error}</p>
            </div>
          )}
        </div>

        <div className="bg-muted/20 flex items-center justify-end gap-3 border-t p-6">
          <Button variant="outline" onClick={onClose} disabled={isCreating}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={isCreating}>
            {isCreating ? (
              <>
                <div className="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white"></div>
                Creating...
              </>
            ) : (
              <>
                <Save className="mr-2 h-4 w-4" />
                Create Keys
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}
