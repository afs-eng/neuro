import { redirect } from "next/navigation";

export default function SRS2RedirectPage({ params }: { params: { id: string } }) {
  redirect(`/dashboard/tests/srs2/${params.id}/result`);
}
