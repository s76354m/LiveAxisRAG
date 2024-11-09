export interface Project {
  id: number;
  project_id: string;
  region: string;
  status: 'Active' | 'Pending' | 'Completed';
  workflow_entity_id: string;
  created_at: string;
  updated_at: string;
  created_by: string;
}

export interface ProjectTranslation {
  RecordID: number;
  ProjectID: string;
  BenchmarkFileID: string;
  ProjectType: string;
  ProjectDesc: string;
  Analyst: string;
  PM: string;
  GoLiveDate: string;
  MaxMileage: number;
  Status: string;
  NewMarket: string;
  ProvRef: string;
  DataLoadDate: string;
  LastEditDate: string;
  LastEditMSID: string;
  NDB_LOB: string;
  RefreshInd: number;
}

export interface Competitor {
  id: number;
  project_id: string;
  product: string;
  status: 'Draft' | 'Submitted' | 'Approved';
  created_at: string;
  updated_at: string;
  created_by: string;
}

export interface CompetitorTranslation {
  RecordID: number;
  ProjectID: string;
  ProjectStatus: string;
  StrenuusProductCode: string;
  Payor: string;
  Product: string;
  EI: boolean;
  CS: boolean;
  MR: boolean;
  DataLoadDate: string;
  LastEditMSID: string;
}

export interface ProjectNote {
  RecordID: number;
  ProjectID: string;
  Notes: string;
  ActionItem: string;
  ProjectStatus: string;
  DataLoadDate: string;
  LastEditDate: string;
  OrigNoteMSID: string;
  LastEditMSID: string;
  ProjectCategory: string;
} 