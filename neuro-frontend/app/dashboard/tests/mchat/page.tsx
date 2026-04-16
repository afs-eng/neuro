import { Suspense } from "react";

import MCHATPage from "./page.client";

export default function Page() {
  return (
    <Suspense fallback={<div className="py-16 text-center text-slate-500">Carregando M-CHAT...</div>}>
      <MCHATPage />
    </Suspense>
  );
}
