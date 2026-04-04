import axios from 'axios'

const request = axios.create({
  baseURL: '/api/v1',
  timeout: 60000,
})

request.interceptors.response.use(response => response.data)

export interface InferenceProvenanceRow {
  id: string
  chapter_element_id: string | null
  rule_id: string
  role: string
}

export interface InferenceFactPayload {
  id: string
  subject: string
  predicate: string
  object: string
  chapter_number: number | null
  confidence: number | null
  source_type: string | null
}

export interface InferenceFactBundle {
  fact: InferenceFactPayload
  provenance: InferenceProvenanceRow[]
}

export interface ChapterInferenceEvidenceData {
  story_node_id: string | null
  chapter_number: number
  facts: InferenceFactBundle[]
  hint?: string
}

export const knowledgeGraphApi = {
  getChapterInferenceEvidence(
    novelId: string,
    chapterNumber: number
  ): Promise<{ success: boolean; data: ChapterInferenceEvidenceData }> {
    return request.get(
      `/knowledge-graph/novels/${encodeURIComponent(novelId)}/chapters/by-number/${chapterNumber}/inference-evidence`
    ) as Promise<{ success: boolean; data: ChapterInferenceEvidenceData }>
  },

  revokeChapterInference(
    novelId: string,
    chapterNumber: number
  ): Promise<{
    success: boolean
    data: { removed_provenance_triples: number; deleted_inferred_facts: number }
  }> {
    return request.delete(
      `/knowledge-graph/novels/${encodeURIComponent(novelId)}/chapters/by-number/${chapterNumber}/inference`
    ) as Promise<{
      success: boolean
      data: { removed_provenance_triples: number; deleted_inferred_facts: number }
    }>
  },

  revokeInferredTriple(
    novelId: string,
    tripleId: string
  ): Promise<{ success: boolean; message: string }> {
    return request.delete(
      `/knowledge-graph/novels/${encodeURIComponent(novelId)}/inferred-triples/${encodeURIComponent(tripleId)}`
    ) as Promise<{ success: boolean; message: string }>
  },
}
