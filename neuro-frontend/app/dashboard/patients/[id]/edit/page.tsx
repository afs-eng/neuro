'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import { PageContainer, PageHeader, SectionCard } from '@/components/ui/page';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Save, User, MapPin, Contact, FileText } from 'lucide-react';

const initialFormData = {
  full_name: '',
  birth_date: '',
  sex: '',
  schooling: '',
  school_name: '',
  grade_year: '',
  mother_name: '',
  father_name: '',
  phone: '',
  email: '',
  city: '',
  state: '',
  responsible_name: '',
  responsible_phone: '',
  notes: '',
};

export default function EditPatientPage() {
  const params = useParams();
  const router = useRouter();
  const patientId = params.id as string;
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState(initialFormData);

  useEffect(() => {
    async function fetchPatient() {
      try {
        setLoading(true);
        const patient = await api.get<any>(`/api/patients/${patientId}`);
        setFormData({
          full_name: patient.full_name || '',
          birth_date: patient.birth_date || '',
          sex: patient.sex || '',
          schooling: patient.schooling || '',
          school_name: patient.school_name || '',
          grade_year: patient.grade_year || '',
          mother_name: patient.mother_name || '',
          father_name: patient.father_name || '',
          phone: patient.phone || '',
          email: patient.email || '',
          city: patient.city || '',
          state: patient.state || '',
          responsible_name: patient.responsible_name || '',
          responsible_phone: patient.responsible_phone || '',
          notes: patient.notes || '',
        });
      } catch (err: any) {
        setError(err?.message || 'Erro ao carregar paciente');
      } finally {
        setLoading(false);
      }
    }

    if (patientId) {
      fetchPatient();
    }
  }, [patientId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError('');

    try {
      await api.patch(`/api/patients/${patientId}`, formData);
      router.push(`/dashboard/patients/${patientId}`);
    } catch (err: any) {
      setError(err?.message || 'Erro ao salvar alterações do paciente');
    } finally {
      setSaving(false);
    }
  };

  const labelStyle = "text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2 block";
  const inputStyle = "w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-bold text-slate-700 outline-none focus:ring-2 focus:ring-primary/20 transition-all";

  return (
    <PageContainer>
      <PageHeader
        title="Editar Paciente"
        subtitle="Atualize os dados cadastrais e clínicos do prontuário."
        actions={
          <Link href={`/dashboard/patients/${patientId}`}>
            <Button variant="ghost" className="gap-2 font-bold text-slate-500">
              <ArrowLeft className="h-4 w-4" />
              Voltar
            </Button>
          </Link>
        }
      />

      {loading ? (
        <div className="flex flex-col items-center justify-center py-24 gap-4">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-100 border-t-primary"></div>
          <p className="text-sm font-bold text-slate-400 uppercase tracking-widest animate-pulse">Carregando Prontuário...</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-8 animate-in fade-in duration-700">
          {error && (
            <div className="rounded-2xl bg-rose-50 border border-rose-100 p-4 text-xs font-black uppercase tracking-widest text-rose-500 text-center">
              {String(error)}
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <SectionCard title="Dados Pessoais" description="Identificação básica e escolaridade do paciente." icon={<User className="h-5 w-5 text-primary" />}>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="sm:col-span-2">
                  <label className={labelStyle}>Nome Completo *</label>
                  <input name="full_name" value={formData.full_name} onChange={handleChange} required className={inputStyle} />
                </div>
                <div>
                  <label className={labelStyle}>Data de Nascimento *</label>
                  <input name="birth_date" type="date" value={formData.birth_date} onChange={handleChange} required className={inputStyle} />
                </div>
                <div>
                  <label className={labelStyle}>Sexo *</label>
                  <select name="sex" value={formData.sex} onChange={handleChange} required className={inputStyle}>
                    <option value="">Selecione...</option>
                    <option value="M">Masculino</option>
                    <option value="F">Feminino</option>
                    <option value="O">Outro</option>
                  </select>
                </div>
                <div className="sm:col-span-2">
                  <label className={labelStyle}>Escolaridade *</label>
                  <select name="schooling" value={formData.schooling} onChange={handleChange} required className={inputStyle}>
                    <option value="">Selecione...</option>
                    <option value="infantil">Educação Infantil</option>
                    <option value="fundamental_incompleto">Fundamental Incompleto</option>
                    <option value="fundamental_completo">Fundamental Completo</option>
                    <option value="medio_incompleto">Médio Incompleto</option>
                    <option value="medio_completo">Médio Completo</option>
                    <option value="superior_incompleto">Superior Incompleto</option>
                    <option value="superior_completo">Superior Completo</option>
                    <option value="pos_graduacao">Pós-graduação</option>
                  </select>
                </div>
                <div>
                  <label className={labelStyle}>Nome da Escola</label>
                  <input name="school_name" value={formData.school_name} onChange={handleChange} className={inputStyle} />
                </div>
                <div>
                  <label className={labelStyle}>Série/Ano</label>
                  <input name="grade_year" value={formData.grade_year} onChange={handleChange} className={inputStyle} />
                </div>
              </div>
            </SectionCard>

            <SectionCard title="Contato & Localização" description="Informações para comunicação e logística." icon={<MapPin className="h-5 w-5 text-primary" />}>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                  <label className={labelStyle}>Telefone</label>
                  <input name="phone" type="tel" value={formData.phone} onChange={handleChange} className={inputStyle} />
                </div>
                <div>
                  <label className={labelStyle}>E-mail</label>
                  <input name="email" type="email" value={formData.email} onChange={handleChange} className={inputStyle} />
                </div>
                <div>
                  <label className={labelStyle}>Cidade</label>
                  <input name="city" value={formData.city} onChange={handleChange} className={inputStyle} />
                </div>
                <div>
                  <label className={labelStyle}>Estado (UF)</label>
                  <input name="state" value={formData.state} onChange={handleChange} maxLength={2} className={inputStyle} />
                </div>
              </div>
            </SectionCard>

            <SectionCard title="Núcleo Familiar" description="Informações sobre pais e responsáveis." icon={<Contact className="h-5 w-5 text-primary" />}>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                  <label className={labelStyle}>Nome da Mãe</label>
                  <input name="mother_name" value={formData.mother_name} onChange={handleChange} className={inputStyle} />
                </div>
                <div>
                  <label className={labelStyle}>Nome do Pai</label>
                  <input name="father_name" value={formData.father_name} onChange={handleChange} className={inputStyle} />
                </div>
                <div>
                  <label className={labelStyle}>Responsável Direto</label>
                  <input name="responsible_name" value={formData.responsible_name} onChange={handleChange} className={inputStyle} />
                </div>
                <div>
                  <label className={labelStyle}>Telefone do Responsável</label>
                  <input name="responsible_phone" type="tel" value={formData.responsible_phone} onChange={handleChange} className={inputStyle} />
                </div>
              </div>
            </SectionCard>

            <SectionCard title="Observações Clínicas" description="Notas e histórico relevante." icon={<FileText className="h-5 w-5 text-primary" />}>
              <div className="space-y-4">
                <label className={labelStyle}>Notas</label>
                <textarea name="notes" value={formData.notes} onChange={handleChange} className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-600 outline-none focus:ring-2 focus:ring-primary/20 transition-all min-h-[160px]" />
              </div>
            </SectionCard>
          </div>

          <div className="flex justify-end pt-8 border-t border-slate-100">
            <Button type="submit" disabled={saving} className="px-12 h-14 rounded-2xl font-black uppercase tracking-widest gap-3 shadow-spike border-none text-white">
              <Save className="h-5 w-5" />
              {saving ? 'Salvando...' : 'Salvar Alterações'}
            </Button>
          </div>
        </form>
      )}
    </PageContainer>
  );
}
