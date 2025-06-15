import { useState, useEffect } from 'react';
import { getProjects, getProjectTranslations } from '@/services/api';
import type { Translation, Project } from '@/types/api';
import { ChevronDown, Loader2 } from 'lucide-react';

interface ProjectSelectorProps {
  projectId: string;
  onProjectSelect: (projectId: string) => void;
  onTranslationsLoad: (translations: Translation[]) => void;
  onLoadingChange: (isLoading: boolean) => void;
  onError: (error: string | null) => void;
}

export function ProjectSelector({
  projectId,
  onProjectSelect,
  onTranslationsLoad,
  onLoadingChange,
  onError,
}: ProjectSelectorProps) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [isLoadingProjects, setIsLoadingProjects] = useState(true);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  // Load projects on component mount
  useEffect(() => {
    const loadProjects = async () => {
      try {
        setIsLoadingProjects(true);
        const response = await getProjects({
          include_statistics: 1,
          include_settings: 1,
          limit: 100,
        });
        setProjects(response.projects);

        // If there's a current projectId, find and select it
        if (projectId) {
          const currentProject = response.projects.find((p) => p.project_id === projectId);
          if (currentProject) {
            setSelectedProject(currentProject);
          }
        }
      } catch (error) {
        console.error('Failed to load projects:', error);
        onError('Failed to load projects. Please check your connection and try again.');
      } finally {
        setIsLoadingProjects(false);
      }
    };

    loadProjects();
  }, [projectId, onError]);

  const handleProjectSelect = (project: Project) => {
    setSelectedProject(project);
    setIsDropdownOpen(false);
    onProjectSelect(project.project_id);

    // Automatically load translations when project is selected
    loadTranslationsForProject(project);
  };

  const loadTranslationsForProject = async (project: Project) => {
    onLoadingChange(true);
    onError(null);

    try {
      const translations = await getProjectTranslations({
        project_id: project.project_id,
        limit: 100,
        page: 1,
      });

      onTranslationsLoad(translations);
    } catch (error) {
      console.error('Failed to load translations:', error);
      onError(error instanceof Error ? error.message : 'Failed to load translations');
    } finally {
      onLoadingChange(false);
    }
  };

  if (isLoadingProjects) {
    return (
      <div className="rounded-lg border p-6 shadow-sm">
        <div className="flex items-center justify-center py-4">
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          <span>Loading projects...</span>
        </div>
      </div>
    );
  }

  if (projects.length === 0) {
    return (
      <div className="rounded-lg border p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold">Project Selection</h2>
        <div className="py-4 text-center">
          <p className="text-muted-foreground">
            No projects found. Please check your API configuration.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-lg border p-6 shadow-sm">
      <h2 className="mb-4 text-xl font-semibold">Project Selection</h2>

      <div className="flex items-end gap-4">
        <div className="flex-1">
          <label htmlFor="project-select" className="mb-2 block text-sm font-medium">
            Select Project
          </label>
          <div className="relative">
            <button
              id="project-select"
              type="button"
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="border-input focus:ring-ring focus:border-ring flex w-full items-center justify-between rounded-md border px-3 py-2 shadow-sm focus:ring-2 focus:outline-none"
            >
              <span className="truncate">
                {selectedProject ? selectedProject.name : 'Choose a project...'}
              </span>
              <ChevronDown
                className={`h-4 w-4 transition-transform ${isDropdownOpen ? 'rotate-180' : ''}`}
              />
            </button>

            {isDropdownOpen && (
              <div className="bg-background absolute top-full right-0 left-0 z-50 mt-1 max-h-60 overflow-auto rounded-md border shadow-lg">
                {projects.map((project) => (
                  <button
                    key={project.project_id}
                    type="button"
                    onClick={() => handleProjectSelect(project)}
                    className="hover:bg-accent hover:text-accent-foreground w-full px-3 py-2 text-left transition-colors"
                  >
                    <div>
                      <div className="font-medium">{project.name}</div>
                      <div className="text-muted-foreground text-sm">
                        {project.description || 'No description'}
                      </div>
                      <div className="text-muted-foreground mt-1 flex items-center gap-4 text-xs">
                        <span>ID: {project.project_id}</span>
                        {project.statistics && (
                          <>
                            <span>Keys: {project.statistics.keys_total}</span>
                            <span>Progress: {project.statistics.progress_total}%</span>
                          </>
                        )}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {selectedProject && (
        <div className="bg-muted mt-4 rounded-md p-3">
          <div className="grid grid-cols-1 gap-2 text-sm md:grid-cols-2">
            <div>
              <span className="text-muted-foreground">Project:</span>
              <span className="ml-2 font-medium">{selectedProject.name}</span>
            </div>
            <div>
              <span className="text-muted-foreground">ID:</span>
              <span className="ml-2 font-mono text-xs">{selectedProject.project_id}</span>
            </div>
            <div>
              <span className="text-muted-foreground">Base Language:</span>
              <span className="ml-2">{selectedProject.base_language_iso.toUpperCase()}</span>
            </div>
            {selectedProject.statistics && (
              <div>
                <span className="text-muted-foreground">Keys:</span>
                <span className="ml-2">{selectedProject.statistics.keys_total}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
