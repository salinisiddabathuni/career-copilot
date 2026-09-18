"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [resumeId, setResumeId] = useState<number | null>(null);
  const [skills, setSkills] = useState<string[]>([]);
  const [error, setError] = useState("");
  const [gapResults, setGapResults] = useState<any[]>([]);

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/resume/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();

      if (data.error) {
        setError(data.error);
      } else {
        setResumeId(data.id);
        setSkills(data.extracted_skills);

        const gapRes = await fetch(`http://127.0.0.1:8000/gap-analysis/${data.id}`);
        const gapData = await gapRes.json();
        setGapResults(gapData.results);
      }
    } catch (err) {
      setError("Could not reach the backend. Is it running?");
    } finally {
      setUploading(false);
    }
  };

  const tierClass = (score: number) =>
    score >= 70 ? "tier-high" : score >= 40 ? "tier-mid" : "tier-low";

  return (
    <main style={{ padding: "3rem 1.5rem", maxWidth: "720px", margin: "0 auto" }}>
      <h1 className="font-display" style={{ fontSize: "2rem", marginBottom: "0.4rem" }}>
        Career Copilot
      </h1>
      <p style={{ color: "var(--text-muted)", marginBottom: "2rem" }}>
        See exactly where your resume stands against real opportunities — and what's missing.
      </p>

      <div className="upload-console">
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          style={{
            marginLeft: "1rem",
            background: "var(--accent)",
            color: "#0F1420",
            border: "none",
            padding: "0.5rem 1rem",
            borderRadius: "6px",
            fontWeight: 600,
            cursor: file ? "pointer" : "not-allowed",
          }}
        >
          {uploading ? "Uploading..." : "Upload Resume"}
        </button>
      </div>

      {error && <p style={{ color: "var(--missing)", marginTop: "1rem" }}>{error}</p>}

      {resumeId && (
        <div style={{ marginTop: "2.5rem" }}>
          <h2 className="font-display" style={{ fontSize: "1.3rem", marginBottom: "0.8rem" }}>
            Extracted Skills
          </h2>
          <div>
            {skills.map((skill, i) => (
              <span key={i} className="chip chip-good">{skill}</span>
            ))}
          </div>
        </div>
      )}

      {gapResults.length > 0 && (
        <div style={{ marginTop: "2.5rem" }}>
          <h2 className="font-display" style={{ fontSize: "1.3rem", marginBottom: "1rem" }}>
            Recommended Opportunities
          </h2>
          {gapResults.map((opp) => (
            <div key={opp.opportunity_id} className={`opp-row ${tierClass(opp.match_score)}`}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
                <h3 className="font-display" style={{ fontSize: "1.05rem" }}>
                  {opp.title} <span style={{ color: "var(--text-muted)", fontWeight: 400 }}>· {opp.type}</span>
                </h3>
                <span style={{ fontFamily: "monospace", color: "var(--accent)" }}>{opp.match_score}%</span>
              </div>

              <div className="meter">
                <div className="meter-fill" style={{ width: `${opp.match_score}%` }} />
              </div>

              <div>
                {opp.matched_skills.map((s: string, i: number) => (
                  <span key={i} className="chip chip-good">{s}</span>
                ))}
                {opp.missing_skills.map((s: string, i: number) => (
                  <span key={i} className="chip chip-missing">{s}</span>
                ))}
              </div>

              <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", marginTop: "0.6rem" }}>
                Deadline: {opp.deadline} ·{" "}
                <a href={opp.url} target="_blank" rel="noopener noreferrer" style={{ color: "var(--accent)" }}>
                  View opportunity
                </a>
              </p>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}