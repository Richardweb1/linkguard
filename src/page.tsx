"use client";

import { useState } from "react";

export default function Home() {
  const [wallet, setWallet] = useState("");
  const [username, setUsername] = useState("");
  const [domain, setDomain] = useState("");
  const [submitted, setSubmitted] = useState(false);

  function submitCheck() {
    if (!wallet || !username || !domain) return;
    setSubmitted(true);
  }

  return (
    <main className="min-h-screen bg-black text-white">
      <section className="mx-auto flex min-h-screen max-w-4xl flex-col items-center justify-center px-6">
        <div className="mb-6 rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-2 text-sm text-emerald-300">
          Web3 reputation check
        </div>

        <h1 className="text-center text-5xl font-bold tracking-tight md:text-7xl">
          Check a wallet, username, or domain before you trust it.
        </h1>

        <p className="mt-6 max-w-2xl text-center text-lg text-zinc-400">
          Submit public information and get a simple trust preview for scams,
          impersonation, suspicious domains, or risky wallet behavior.
        </p>

        <div className="mt-10 w-full max-w-2xl rounded-2xl border border-white/10 bg-white/5 p-5">
          <div className="space-y-4">
            <input
              value={wallet}
              onChange={(e) => setWallet(e.target.value)}
              placeholder="Wallet address"
              className="w-full rounded-xl bg-black px-4 py-4 text-white outline-none placeholder:text-zinc-600"
            />

            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username / handle"
              className="w-full rounded-xl bg-black px-4 py-4 text-white outline-none placeholder:text-zinc-600"
            />

            <input
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              placeholder="Domain or link"
              className="w-full rounded-xl bg-black px-4 py-4 text-white outline-none placeholder:text-zinc-600"
            />

            <button
              onClick={submitCheck}
              className="w-full rounded-xl bg-emerald-400 px-6 py-4 font-semibold text-black transition hover:bg-emerald-300"
            >
              Submit Check
            </button>
          </div>
        </div>

        {submitted && (
          <div className="mt-8 w-full max-w-2xl rounded-2xl border border-yellow-400/30 bg-yellow-400/10 p-6">
            <p className="text-sm text-zinc-400">Submission received</p>
            <h2 className="mt-2 text-3xl font-bold text-yellow-300">
              Pending Review
            </h2>

            <div className="mt-4 space-y-2 text-zinc-300">
              <p><strong>Wallet:</strong> {wallet}</p>
              <p><strong>Username:</strong> {username}</p>
              <p><strong>Domain:</strong> {domain}</p>
            </div>

            <p className="mt-4 text-zinc-400">
              Next we will connect this form to a database so every submission is saved.
            </p>
          </div>
        )}
      </section>
    </main>
  );
}