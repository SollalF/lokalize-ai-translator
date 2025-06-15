import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { evaluateTranslation } from '@/services/api';
import type { Translation, TranslationEvaluationResponse } from '@/types/api';
import {
  X,
  Star,
  AlertTriangle,
  CheckCircle,
  MessageSquare,
  TrendingUp,
  Target,
  Lightbulb,
} from 'lucide-react';

interface TranslationEvaluationModalProps {
  translation: Translation;
  sourceText: string;
  projectId: string;
  onClose: () => void;
}

export function TranslationEvaluationModal({
  translation,
  sourceText,
  projectId,
  onClose,
}: TranslationEvaluationModalProps) {
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [evaluation, setEvaluation] = useState<TranslationEvaluationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleEvaluate = async () => {
    if (!translation.translation || !sourceText) {
      setError('Missing source text or translation');
      return;
    }

    setIsEvaluating(true);
    setError(null);

    try {
      const result = await evaluateTranslation({
        source_text: sourceText,
        source_lang: 'en',
        translated_text: translation.translation,
        target_lang: translation.language_iso.split('_')[0], // Get base language code
        project_id: projectId,
      });

      setEvaluation(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to evaluate translation');
    } finally {
      setIsEvaluating(false);
    }
  };

  const formatScore = (score: number | null) => {
    if (score === null) return 'N/A';
    return score.toFixed(2);
  };

  const getComplianceColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="bg-background max-h-[90vh] w-full max-w-4xl overflow-y-auto rounded-lg shadow-lg">
        <div className="flex items-center justify-between border-b p-6">
          <div>
            <h2 className="text-xl font-semibold">Translation Evaluation</h2>
            <p className="text-muted-foreground text-sm">
              Language: <span className="font-mono font-medium">{translation.language_iso}</span>
            </p>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>

        <div className="space-y-6 p-6">
          {/* Source and Translation Display */}
          <div className="space-y-4">
            <div>
              <label className="mb-2 block text-sm font-medium">Source Text (English)</label>
              <div className="bg-muted rounded-md p-3">
                <p className="text-sm">{sourceText}</p>
              </div>
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">
                Translation ({translation.language_iso})
              </label>
              <div className="bg-muted rounded-md p-3">
                <p className="text-sm">{translation.translation}</p>
              </div>
            </div>
          </div>

          {/* Evaluate Button */}
          {!evaluation && (
            <div className="flex justify-center">
              <Button onClick={handleEvaluate} disabled={isEvaluating} size="lg">
                {isEvaluating ? (
                  <>
                    <div className="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white"></div>
                    Evaluating...
                  </>
                ) : (
                  <>
                    <MessageSquare className="mr-2 h-4 w-4" />
                    Get LLM Feedback
                  </>
                )}
              </Button>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="border-destructive bg-destructive/10 flex items-center gap-2 rounded-lg border p-3">
              <AlertTriangle className="text-destructive h-4 w-4" />
              <p className="text-destructive text-sm">{error}</p>
            </div>
          )}

          {/* Evaluation Results */}
          {evaluation && (
            <div className="space-y-6">
              {/* Overall Assessment */}
              <div className="border-primary bg-primary/5 rounded-lg border p-4">
                <h3 className="mb-2 flex items-center gap-2 font-medium">
                  <Target className="h-4 w-4" />
                  Overall Assessment
                </h3>
                <p className="text-sm">{evaluation.overall_assessment}</p>
              </div>

              {/* Metric Scores */}
              <div className="rounded-lg border p-4">
                <h3 className="mb-3 flex items-center gap-2 font-medium">
                  <TrendingUp className="h-4 w-4" />
                  Metric Scores
                </h3>
                <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
                  <div className="text-center">
                    <p className="text-muted-foreground text-sm">BLEU</p>
                    <p className="font-medium">{formatScore(evaluation.metric_scores.bleu)}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-muted-foreground text-sm">TER</p>
                    <p className="font-medium">{formatScore(evaluation.metric_scores.ter)}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-muted-foreground text-sm">chrF</p>
                    <p className="font-medium">{formatScore(evaluation.metric_scores.chrf)}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-muted-foreground text-sm">Edit Distance</p>
                    <p className="font-medium">
                      {formatScore(evaluation.metric_scores.edit_distance)}
                    </p>
                  </div>
                </div>
              </div>

              {/* Glossary Compliance */}
              <div className="rounded-lg border p-4">
                <h3 className="mb-3 flex items-center gap-2 font-medium">
                  <CheckCircle className="h-4 w-4" />
                  Glossary Compliance
                </h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Compliance Score:</span>
                    <span
                      className={`font-medium ${getComplianceColor(evaluation.glossary_compliance.compliance_score)}`}
                    >
                      {evaluation.glossary_compliance.compliance_score}%
                    </span>
                  </div>
                  <p className="text-sm">{evaluation.glossary_compliance.compliance_summary}</p>

                  {evaluation.glossary_compliance.terms_found_in_source.length > 0 && (
                    <div>
                      <p className="mb-2 text-sm font-medium">Terms Found:</p>
                      <div className="space-y-2">
                        {evaluation.glossary_compliance.terms_found_in_source.map((term, index) => (
                          <div key={index} className="bg-muted rounded p-2 text-sm">
                            <div className="flex items-center justify-between">
                              <span className="font-mono">{term.term}</span>
                              <span className="text-muted-foreground text-xs">
                                {term.case_sensitive ? 'Case-sensitive' : 'Case-insensitive'}
                                {term.forbidden && ' | Forbidden'}
                                {!term.translatable && ' | Non-translatable'}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* LLM Feedback */}
              <div className="rounded-lg border p-4">
                <h3 className="mb-3 flex items-center gap-2 font-medium">
                  <MessageSquare className="h-4 w-4" />
                  LLM Feedback
                </h3>

                <div className="space-y-4">
                  {/* Summary */}
                  <div>
                    <h4 className="mb-2 text-sm font-medium">Summary</h4>
                    <p className="bg-muted rounded p-3 text-sm">
                      {evaluation.llm_feedback.summary}
                    </p>
                  </div>

                  {/* Strengths */}
                  {evaluation.llm_feedback.strengths.length > 0 && (
                    <div>
                      <h4 className="mb-2 flex items-center gap-1 text-sm font-medium">
                        <Star className="h-3 w-3 text-green-600" />
                        Strengths
                      </h4>
                      <ul className="space-y-1">
                        {evaluation.llm_feedback.strengths.map((strength, index) => (
                          <li key={index} className="text-sm text-green-700">
                            • {strength}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Weaknesses */}
                  {evaluation.llm_feedback.weaknesses.length > 0 && (
                    <div>
                      <h4 className="mb-2 flex items-center gap-1 text-sm font-medium">
                        <AlertTriangle className="h-3 w-3 text-orange-600" />
                        Areas for Improvement
                      </h4>
                      <ul className="space-y-1">
                        {evaluation.llm_feedback.weaknesses.map((weakness, index) => (
                          <li key={index} className="text-sm text-orange-700">
                            • {weakness}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Specific Comments */}
                  {evaluation.llm_feedback.specific_comments.length > 0 && (
                    <div>
                      <h4 className="mb-2 text-sm font-medium">Specific Comments</h4>
                      <div className="space-y-2">
                        {evaluation.llm_feedback.specific_comments.map((comment, index) => (
                          <div key={index} className="bg-muted rounded p-3">
                            <p className="mb-1 font-mono text-sm font-medium">"{comment.part}"</p>
                            <p className="text-sm">{comment.comment}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Suggestions */}
                  {evaluation.llm_feedback.suggestions.length > 0 && (
                    <div>
                      <h4 className="mb-2 flex items-center gap-1 text-sm font-medium">
                        <Lightbulb className="h-3 w-3 text-blue-600" />
                        Suggestions
                      </h4>
                      <ul className="space-y-1">
                        {evaluation.llm_feedback.suggestions.map((suggestion, index) => (
                          <li key={index} className="text-sm text-blue-700">
                            • {suggestion}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="bg-muted/20 flex items-center justify-end gap-3 border-t p-6">
          <Button variant="outline" onClick={onClose}>
            Close
          </Button>
          {evaluation && (
            <Button
              onClick={() => {
                setEvaluation(null);
                setError(null);
              }}
            >
              Evaluate Again
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
