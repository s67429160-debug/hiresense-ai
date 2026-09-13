import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "https://hiresense-ai-backend-docker.onrender.com/api/v1";

function App() {
  const [isLogin, setIsLogin] = useState(true);

  const [loggedIn, setLoggedIn] = useState(
    Boolean(localStorage.getItem("token"))
  );

  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
  });

  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [profile, setProfile] = useState(null);

  const [showHistory, setShowHistory] = useState(false);
  const [showProfile, setShowProfile] = useState(false);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // =========================
  // FORM CHANGE
  // =========================

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  // =========================
  // LOGIN / REGISTER
  // =========================

  const handleAuth = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      if (isLogin) {
        const response = await axios.post(
          `${API_URL}/auth/login`,
          new URLSearchParams({
            username: form.email,
            password: form.password,
          }),
          {
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
          }
        );

        localStorage.setItem("token", response.data.access_token);

        setLoggedIn(true);
        setMessage("Login successful!");
      } else {
        await axios.post(`${API_URL}/auth/register`, {
          full_name: form.full_name,
          email: form.email,
          password: form.password,
        });

        setMessage("Registration successful. Please login.");

        setIsLogin(true);

        setForm({
          full_name: "",
          email: form.email,
          password: "",
        });
      }
    } catch (error) {
      setMessage(
        error.response?.data?.detail ||
          "Something went wrong."
      );
    }
  };

  // =========================
  // LOGOUT
  // =========================

  const logout = () => {
    localStorage.removeItem("token");

    setLoggedIn(false);
    setResult(null);
    setHistory([]);
    setProfile(null);

    setShowHistory(false);
    setShowProfile(false);
  };

  // =========================
  // UPLOAD RESUME
  // =========================

  const uploadResume = async () => {
    if (!resume) {
      setMessage("Please select a PDF resume first.");
      return;
    }

    const token = localStorage.getItem("token");

    if (!token) {
      setMessage("Please login again.");
      return;
    }

    const formData = new FormData();

    formData.append("file", resume);

    setLoading(true);
    setMessage("");

    try {
      const response = await axios.post(
        `${API_URL}/resume/upload`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setMessage(
        `Resume uploaded successfully: ${response.data.filename}`
      );
    } catch (error) {
      setMessage(
        error.response?.data?.detail ||
          "Resume upload failed."
      );
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // ANALYZE RESUME
  // =========================

  const analyzeResume = async () => {
    if (!jobDescription.trim()) {
      setMessage("Please enter a job description.");
      return;
    }

    const token = localStorage.getItem("token");

    if (!token) {
      setMessage("Please login again.");
      return;
    }

    setLoading(true);
    setMessage("");
    setResult(null);

    try {
      const response = await axios.post(
        `${API_URL}/analysis/`,
        {
          job_description: jobDescription,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setResult(response.data);

      setMessage(
        "Resume analysis completed successfully."
      );

      loadProfile();
    } catch (error) {
      setMessage(
        error.response?.data?.detail ||
          "Resume analysis failed."
      );
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // DOWNLOAD ATS REPORT
  // =========================

  const downloadReport = async () => {
  if (!result?.analysis_id) {
    setMessage("No analysis report available.");
    return;
  }

  const token = localStorage.getItem("token");

  if (!token) {
    setMessage("Please login again.");
    return;
  }

  try {
    setLoading(true);
    setMessage("Generating ATS report...");

    const response = await axios.get(
      `${API_URL}/analysis/${result.analysis_id}/report`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        responseType: "blob",
      }
    );

    const blob = new Blob(
      [response.data],
      { type: "application/pdf" }
    );

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = `HireSense_ATS_Report_${result.analysis_id}.pdf`;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    window.URL.revokeObjectURL(url);

    setMessage("ATS report downloaded successfully.");
  } catch (error) {
    console.error("PDF ERROR:", error);

    if (error.response?.status === 401) {
      setMessage("Session expired. Please login again.");
    } else {
      setMessage("Could not generate ATS report.");
    }
  } finally {
    setLoading(false);
  }
};

  // =========================
  // DOWNLOAD HISTORY REPORT
  // =========================

  const downloadHistoryReport = async (analysisId) => {
    if (!analysisId) {
      setMessage("No analysis report available.");
      return;
    }

    const token = localStorage.getItem("token");

    if (!token) {
      setMessage("Please login again.");
      return;
    }

    try {
      setLoading(true);
      setMessage("Generating ATS report...");

      const response = await axios.get(
        `${API_URL}/analysis/${analysisId}/report`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          responseType: "blob",
        }
      );

      const blob = new Blob(
        [response.data],
        { type: "application/pdf" }
      );

      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.download = `HireSense_ATS_Report_${analysisId}.pdf`;

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      window.URL.revokeObjectURL(url);

      setMessage("ATS report downloaded successfully.");
    } catch (error) {
      console.error("HISTORY PDF ERROR:", error);

      if (error.response?.status === 401) {
        setMessage("Session expired. Please login again.");
      } else {
        setMessage("Could not generate ATS report.");
      }
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // LOAD HISTORY
  // =========================

  const loadHistory = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      setMessage("Please login again.");
      return;
    }

    try {
      const response = await axios.get(
        `${API_URL}/analysis/history`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setHistory(
        response.data.history || []
      );

      setShowHistory(true);
      setShowProfile(false);
      setResult(null);
    } catch (error) {
      setMessage(
        error.response?.data?.detail ||
          "Could not load analysis history."
      );
    }
  };

  // =========================
  // LOAD PROFILE
  // =========================

  const loadProfile = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      return;
    }

    try {
      const response = await axios.get(
        `${API_URL}/profile/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setProfile(response.data);

      setShowProfile(true);
      setShowHistory(false);
    } catch (error) {
      setMessage(
        error.response?.data?.detail ||
          "Could not load profile."
      );
    }
  };

  // =========================
  // SCORE CLASS
  // =========================

  const getScoreClass = (score) => {
    if (score >= 80) {
      return "score-good";
    }

    if (score >= 60) {
      return "score-medium";
    }

    return "score-low";
  };

  // =========================
  // LOGIN PAGE
  // =========================

  if (!loggedIn) {
    return (
      <div className="app auth-page">
        <div className="auth-container">

          <div className="auth-logo">
            <div className="logo-icon">
              H
            </div>

            <div>
              <h1>HireSense AI</h1>

              <p>
                AI-Powered Resume Intelligence
              </p>
            </div>
          </div>

          <div className="auth-card">

            <div className="auth-tabs">

              <button
                className={
                  isLogin
                    ? "active-tab"
                    : ""
                }
                onClick={() => {
                  setIsLogin(true);
                  setMessage("");
                }}
              >
                Login
              </button>

              <button
                className={
                  !isLogin
                    ? "active-tab"
                    : ""
                }
                onClick={() => {
                  setIsLogin(false);
                  setMessage("");
                }}
              >
                Register
              </button>

            </div>

            <form onSubmit={handleAuth}>

              {!isLogin && (
                <div className="input-group">

                  <label>
                    Full Name
                  </label>

                  <input
                    type="text"
                    name="full_name"
                    placeholder="Enter your full name"
                    value={form.full_name}
                    onChange={handleChange}
                    required
                  />

                </div>
              )}

              <div className="input-group">

                <label>
                  Email
                </label>

                <input
                  type="email"
                  name="email"
                  placeholder="Enter your email"
                  value={form.email}
                  onChange={handleChange}
                  required
                />

              </div>

              <div className="input-group">

                <label>
                  Password
                </label>

                <input
                  type="password"
                  name="password"
                  placeholder="Enter your password"
                  value={form.password}
                  onChange={handleChange}
                  required
                />

              </div>

              <button
                className="primary-button auth-button"
                type="submit"
              >
                {isLogin
                  ? "Login"
                  : "Create Account"}
              </button>

            </form>

            {message && (
              <div className="message">
                {message}
              </div>
            )}

          </div>

          <p className="auth-footer">
            © 2026 HireSense AI
          </p>

        </div>
      </div>
    );
  }

  // =========================
  // DASHBOARD
  // =========================

  return (
    <div className="app dashboard-page">

      {/* NAVBAR */}

      <nav className="navbar">

        <div className="navbar-brand">

          <div className="logo-icon small">
            H
          </div>

          <div>
            <h2>HireSense AI</h2>

            <span>
              Resume Intelligence Platform
            </span>
          </div>

        </div>

        <div className="navbar-actions">

          <button
            className="nav-button"
            onClick={() => {
              setShowProfile(false);
              setShowHistory(false);
              setResult(null);
            }}
          >
            Analyzer
          </button>

          <button
            className="nav-button"
            onClick={loadProfile}
          >
            Profile
          </button>

          <button
            className="nav-button"
            onClick={loadHistory}
          >
            History
          </button>

          <button
            className="logout-button"
            onClick={logout}
          >
            Logout
          </button>

        </div>

      </nav>

      <main className="dashboard-container">

        {/* HEADER */}

        <section className="dashboard-header">

          <div>

            <p className="eyebrow">
              AI-POWERED CAREER ANALYSIS
            </p>

            <h1>
              Find out how well your resume
              <span> matches the job.</span>
            </h1>

            <p className="dashboard-description">
              Upload your resume and compare it
              against any job description using
              intelligent ATS scoring and skill analysis.
            </p>

          </div>

        </section>

        {message && (
          <div className="message dashboard-message">
            {message}
          </div>
        )}

        {/* =========================
            PROFILE
        ========================= */}

        {showProfile && profile && (

          <section className="profile-section">

            <div className="profile-header">

              <div>

                <p className="eyebrow">
                  YOUR ACCOUNT
                </p>

                <h2>
                  Profile
                </h2>

              </div>

              <button
                className="secondary-button"
                onClick={() =>
                  setShowProfile(false)
                }
              >
                Close
              </button>

            </div>

            <div className="profile-grid">

              <div className="profile-card">

                <div className="profile-icon">
                  👤
                </div>

                <h3>
                  {profile.user.full_name}
                </h3>

                <p>
                  {profile.user.email}
                </p>

                <small>
                  Member since{" "}
                  {profile.user.created_at
                    ? new Date(
                        profile.user.created_at
                      ).toLocaleDateString()
                    : "N/A"}
                </small>

              </div>

              <div className="profile-card">

                <div className="profile-icon">
                  📄
                </div>

                <h3>
                  Latest Resume
                </h3>

                {profile.latest_resume ? (
                  <>
                    <p>
                      {profile.latest_resume.filename}
                    </p>

                    <small>
                      Uploaded{" "}
                      {profile.latest_resume.created_at
                        ? new Date(
                            profile.latest_resume.created_at
                          ).toLocaleDateString()
                        : "N/A"}
                    </small>
                  </>
                ) : (
                  <p>
                    No resume uploaded yet.
                  </p>
                )}

              </div>

              <div className="profile-card">

                <div className="profile-icon">
                  📊
                </div>

                <h3>
                  Total Analyses
                </h3>

                <strong className="profile-stat">
                  {
                    profile.analysis_stats
                      .total_analyses
                  }
                </strong>

                <small>
                  Resume analyses completed
                </small>

              </div>

              <div className="profile-card">

                <div className="profile-icon">
                  🏆
                </div>

                <h3>
                  Highest ATS Score
                </h3>

                <strong className="profile-stat">

                  {profile.analysis_stats
                    .highest_ats_score !== null
                    ? `${profile.analysis_stats.highest_ats_score}%`
                    : "N/A"}

                </strong>

                <small>
                  Best score achieved
                </small>

              </div>

            </div>

          </section>
        )}

        {/* =========================
            ANALYZER
        ========================= */}

        {!showProfile &&
          !showHistory && (

            <section className="analyzer-section">

              <div className="analyzer-grid">

                {/* RESUME */}

                <div className="analyzer-card">

                  <div className="card-header">

                    <div className="card-number">
                      01
                    </div>

                    <div>

                      <h2>
                        Upload Resume
                      </h2>

                      <p>
                        Upload your latest PDF resume
                      </p>

                    </div>

                  </div>

                  <label className="upload-box">

                    <input
                      type="file"
                      accept=".pdf"
                      onChange={(e) =>
                        setResume(
                          e.target.files?.[0] ||
                          null
                        )
                      }
                    />

                    <div className="upload-icon">
                      ↑
                    </div>

                    <h3>
                      {resume
                        ? resume.name
                        : "Choose your resume"}
                    </h3>

                    <p>
                      PDF files only
                    </p>

                  </label>

                  <button
                    className="primary-button"
                    onClick={uploadResume}
                    disabled={loading}
                  >
                    {loading
                      ? "Uploading..."
                      : "Upload Resume"}
                  </button>

                </div>

                {/* JOB DESCRIPTION */}

                <div className="analyzer-card">

                  <div className="card-header">

                    <div className="card-number">
                      02
                    </div>

                    <div>

                      <h2>
                        Job Description
                      </h2>

                      <p>
                        Paste the target job description
                      </p>

                    </div>

                  </div>

                  <textarea
                    className="job-textarea"
                    placeholder="Paste the job description here..."
                    value={jobDescription}
                    onChange={(e) =>
                      setJobDescription(
                        e.target.value
                      )
                    }
                  />

                  <button
                    className="primary-button"
                    onClick={analyzeResume}
                    disabled={loading}
                  >
                    {loading
                      ? "Analyzing..."
                      : "Analyze Resume"}
                  </button>

                </div>

              </div>

            </section>
          )}

        {/* =========================
            RESULTS
        ========================= */}

        {!showProfile &&
          !showHistory &&
          result && (

            <section className="results-section">

              {/* RESULTS HEADER */}

              <div className="results-header">
<div className="report-download-container">
  <button
    className="primary-button report-button"
    onClick={downloadReport}
    disabled={loading}
  >
    {loading ? "Generating Report..." : "📄 Download ATS Report"}
  </button>
</div>


                  <p className="eyebrow">
                    ANALYSIS COMPLETE
                  </p>

                  <h2>
                    Resume Analysis
                  </h2>

                  <p>
                    {result.filename}
                  </p>

                </div>

              {/* DOWNLOAD BUTTON */}

              <div className="report-download-container">

                <button
                  className="primary-button report-button"
                  onClick={downloadReport}
                  disabled={loading}
                >
                  {loading
                    ? "Generating Report..."
                    : "📄 Download ATS Report"}
                </button>

              </div>

              {/* ATS SCORE */}

              <div className="ats-score-card">

                <div className="ats-score-left">

                  <p className="score-label">
                    ATS SCORE
                  </p>

                  <div
                    className={`ats-score ${getScoreClass(
                      result.ats_score
                    )}`}
                  >
                    {result.ats_score}%
                  </div>

                  <p className="score-description">
                    Overall compatibility between
                    your resume and the job description.
                  </p>

                </div>

                <div className="score-bar-container">

                  <div className="score-bar-background">

                    <div
                      className={`score-bar-fill ${getScoreClass(
                        result.ats_score
                      )}`}
                      style={{
                        width: `${result.ats_score}%`,
                      }}
                    />

                  </div>

                  <div className="score-scale">

                    <span>
                      0
                    </span>

                    <span>
                      50
                    </span>

                    <span>
                      100
                    </span>

                  </div>

                </div>

              </div>

              {/* SCORE BREAKDOWN */}

              {result.score_breakdown && (

                <div className="breakdown-section">

                  <div className="section-heading">

                    <div>

                      <p className="eyebrow">
                        ATS ANALYSIS
                      </p>

                      <h2>
                        Score Breakdown
                      </h2>

                    </div>

                  </div>

                  <div className="breakdown-grid">

                    <div className="breakdown-card">

                      <div className="breakdown-top">

                        <span>
                          🎯 Skill Match
                        </span>

                        <strong>
                          {
                            result.score_breakdown
                              .skill_match
                          }%
                        </strong>

                      </div>

                      <div className="mini-progress">

                        <div
                          style={{
                            width: `${result.score_breakdown.skill_match}%`,
                          }}
                        />

                      </div>

                      <p>
                        Match between required job
                        skills and skills found in
                        your resume.
                      </p>

                    </div>

                    <div className="breakdown-card">

                      <div className="breakdown-top">

                        <span>
                          🔑 Keyword Match
                        </span>

                        <strong>
                          {
                            result.score_breakdown
                              .keyword_match
                          }%
                        </strong>

                      </div>

                      <div className="mini-progress">

                        <div
                          style={{
                            width: `${result.score_breakdown.keyword_match}%`,
                          }}
                        />

                      </div>

                      <p>
                        Match between important
                        job-related keywords and
                        your resume.
                      </p>

                    </div>

                    <div className="breakdown-card">

                      <div className="breakdown-top">

                        <span>
                          👨‍💻 Role Match
                        </span>

                        <strong>
                          {
                            result.score_breakdown
                              .role_match
                          }%
                        </strong>

                      </div>

                      <div className="mini-progress">

                        <div
                          style={{
                            width: `${result.score_breakdown.role_match}%`,
                          }}
                        />

                      </div>

                      <p>
                        How closely your resume
                        matches the target job role.
                      </p>

                    </div>

                    <div className="breakdown-card">

                      <div className="breakdown-top">

                        <span>
                          🎓 Education Match
                        </span>

                        <strong>
                          {
                            result.score_breakdown
                              .education_match
                          }%
                        </strong>

                      </div>

                      <div className="mini-progress">

                        <div
                          style={{
                            width: `${result.score_breakdown.education_match}%`,
                          }}
                        />

                      </div>

                      <p>
                        Compatibility between
                        education requirements and
                        your resume.
                      </p>

                    </div>

                    <div className="breakdown-card">

                      <div className="breakdown-top">

                        <span>
                          📄 Resume Quality
                        </span>

                        <strong>
                          {
                            result.score_breakdown
                              .resume_quality
                          }%
                        </strong>

                      </div>

                      <div className="mini-progress">

                        <div
                          style={{
                            width: `${result.score_breakdown.resume_quality}%`,
                          }}
                        />

                      </div>

                      <p>
                        Presence of important resume
                        sections such as skills,
                        projects and education.
                      </p>

                    </div>

                  </div>

                </div>
              )}

              {/* SKILLS */}

              <div className="skills-section">

                <div className="skills-column">

                  <div className="skills-title">

                    <span>
                      ✓
                    </span>

                    <h3>
                      Matched Skills
                    </h3>

                  </div>

                  <div className="skill-tags">

                    {result.matched_skills?.length > 0 ? (

                      result.matched_skills.map(
                        (skill, index) => (

                          <span
                            className="skill-tag matched"
                            key={index}
                          >
                            {skill}
                          </span>

                        )
                      )

                    ) : (

                      <p>
                        No matched skills found.
                      </p>

                    )}

                  </div>

                </div>

                <div className="skills-column">

                  <div className="skills-title missing-title">

                    <span>
                      ×
                    </span>

                    <h3>
                      Missing Skills
                    </h3>

                  </div>

                  <div className="skill-tags">

                    {result.missing_skills?.length > 0 ? (

                      result.missing_skills.map(
                        (skill, index) => (

                          <span
                            className="skill-tag missing"
                            key={index}
                          >
                            {skill}
                          </span>

                        )
                      )

                    ) : (

                      <p>
                        No missing skills.
                      </p>

                    )}

                  </div>

                </div>

              </div>

              {/* REQUIRED SKILLS */}

              {result.skills_required_by_job?.length > 0 && (

                <div className="details-card">

                  <h3>
                    Skills Required by Job
                  </h3>

                  <div className="skill-tags">

                    {result.skills_required_by_job.map(
                      (skill, index) => (

                        <span
                          className="skill-tag neutral"
                          key={index}
                        >
                          {skill}
                        </span>

                      )
                    )}

                  </div>

                </div>

              )}

              {/* RECOMMENDATIONS */}

              {result.recommendations?.length > 0 && (

                <div className="recommendations-card">

                  <div className="recommendations-header">

                    <span>
                      💡
                    </span>

                    <div>

                      <h3>
                        Recommended Improvements
                      </h3>

                      <p>
                        Focus on these skills to
                        improve your resume match.
                      </p>

                    </div>

                  </div>

                  <div className="recommendation-list">

                    {result.recommendations.map(
                      (recommendation, index) => {

                        const title =
                          recommendation.skill ||
                          recommendation.title ||
                          "Recommended Skill";

                        const reason =
                          recommendation.reason ||
                          recommendation.description ||
                          "";

                        const priority =
                          recommendation.priority ||
                          "Medium";

                        return (

                          <div
                            className="recommendation-item"
                            key={index}
                          >

                            <div>

                              <strong>
                                {title}
                              </strong>

                              {reason && (
                                <p>
                                  {reason}
                                </p>
                              )}

                            </div>

                            <span className="priority">
                              {priority}
                            </span>

                          </div>

                        );
                      }
                    )}

                  </div>

                </div>

              )}

            </section>
          )}

        {/* =========================
            HISTORY
        ========================= */}

        {showHistory &&
          !showProfile && (

            <section className="history-section">

              <div className="history-header">

                <div>

                  <p className="eyebrow">
                    YOUR ACTIVITY
                  </p>

                  <h2>
                    Analysis History
                  </h2>

                  <p>
                    Previous resume analyses
                  </p>

                </div>

                <button
                  className="secondary-button"
                  onClick={() =>
                    setShowHistory(false)
                  }
                >
                  Back to Analyzer
                </button>

              </div>

              {history.length === 0 ? (

                <div className="empty-state">

                  <div className="empty-icon">
                    📊
                  </div>

                  <h3>
                    No analyses yet
                  </h3>

                  <p>
                    Your completed resume analyses
                    will appear here.
                  </p>

                </div>

              ) : (

                <div className="history-list">

                  {history.map((item) => (

                    <div
                      className="history-card"
                      key={item.analysis_id}
                    >

                      <div className="history-main">

                        <div>

                          <p className="history-date">

                            {item.created_at
                              ? new Date(
                                  item.created_at
                                ).toLocaleString()
                              : "Unknown date"}

                          </p>

                          <h3>
                            Resume Analysis #
                            {item.analysis_id}
                          </h3>

                          <p>

                            {item.job_description
                              ? item.job_description.substring(
                                  0,
                                  180
                                )
                              : "No job description"}

                            {item.job_description?.length >
                            180
                              ? "..."
                              : ""}

                          </p>

                        </div>

                        <div
                          className={`history-score ${getScoreClass(
                            item.ats_score
                          )}`}
                        >
                          {item.ats_score}%
                        </div>

                      </div>

                      <div className="history-skills">

                        {item.matched_skills?.length > 0 && (

                          <div>

                            <strong>
                              Matched:
                            </strong>

                            <div className="skill-tags">

                              {item.matched_skills.map(
                                (skill, index) => (

                                  <span
                                    className="skill-tag matched"
                                    key={index}
                                  >
                                    {skill}
                                  </span>

                                )
                              )}

                            </div>

                          </div>

                        )}

                        {item.missing_skills?.length > 0 && (

                          <div>

                            <strong>
                              Missing:
                            </strong>

                            <div className="skill-tags">

                              {item.missing_skills.map(
                                (skill, index) => (

                                  <span
                                    className="skill-tag missing"
                                    key={index}
                                  >
                                    {skill}
                                  </span>

                                )
                              )}

                            </div>

                          </div>

                        )}

                      </div>

                      <div className="history-actions">
                        <button
                          className="primary-button history-report-button"
                          onClick={() =>
                            downloadHistoryReport(item.analysis_id)
                          }
                          disabled={loading}
                        >
                          {loading
                            ? "Generating..."
                            : "📄 Download Report"}
                        </button>
                      </div>

                    </div>

                  ))}

                </div>

              )}

            </section>
          )}

      </main>

      <footer className="app-footer">

        <p>
          HireSense AI • Intelligent Resume Analysis
        </p>

      </footer>

    </div>
  );
}

export default App;