import { redirect } from "next/navigation";

export default function ETDAHPAISResultIdPage({ params }: { params: { id: string } }) {
  let applicationId = params.id;
  let url = `/dashboard/tests/etdah-pais?application_id=${applicationId}&edit=true`
  redirect(url);
}
