import { React, useState } from "react";
import { Col, FloatingLabel, Form, Row } from "react-bootstrap";
import * as bd from "react-basic-design";
import { useNavigate } from "react-router-dom";
import "../styles.scss";

export default function MedicalHealthForm() {
  const apiUrl = process.env.REACT_APP_API_URL;
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    let params = new URL(document.location.toString()).searchParams;
    let token = params.get("token");
    const requestUrl = new URL(apiUrl);
    requestUrl.pathname = `${requestUrl.pathname}submit/`;
    requestUrl.searchParams.append("token", token);

    try {
      const response = await fetch(requestUrl.toString(), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorMessage = await response.text(); // or await response.json() depending on response type
        throw new Error(
          `Network response was not ok: ${response.statusText}. Details: ${errorMessage}`
        );
      }

      const responseData = await response.json(); // Parse the response JSON
      const message = responseData.message || "Operation successful!";
      navigate(`/target-page?message=${encodeURIComponent(message)}`);
    } catch (error) {
      console.error("Error:", error.message);

      if (error.message.includes("Unauthorized")) {
        setError("Unauthorized access");
      } else {
        setError("An unexpected error occurred");
      }
    }
  };

  return (
    <>
      <bd.Paper className="p-3 my-3 mx-auto" style={{ maxWidth: 600 }}>
        <Form autoComplete="on" onSubmit={handleSubmit}>
          <div className="text-primary text-center mb-4">
            <h2 style={{ color: "black" }} className="mt-3">
              Remote Work & Mental Health 🌍🧠
            </h2>
          </div>

          {/* Employee ID */}
          <FloatingLabel label="Employee ID" className="dense mb-3">
            <Form.Control
              name="Employee_ID"
              type="text"
              placeholder="Employee ID"
              required
            />
          </FloatingLabel>

          {/* Age */}
          <FloatingLabel label="Age" className="dense mb-3">
            <Form.Control
              name="Age"
              type="number"
              placeholder="Age"
              min={18}
              max={70}
              step={1}
              required
            />
          </FloatingLabel>

          <Row>
            {/* Gender */}
            <Col md>
              <FloatingLabel label="Gender" className="dense mb-3">
                <Form.Select name="Gender" required>
                  <option value="">Select Gender</option>
                  <option>Non-binary</option>
                  <option>Female</option>
                  <option>Male</option>
                  <option>Prefer not to say</option>
                </Form.Select>
              </FloatingLabel>
            </Col>

            {/* Job Role */}
            <Col md>
              <FloatingLabel label="Job Role" className="dense mb-3">
                <Form.Select name="Job_Role" required>
                  <option value="">Select Job Role</option>
                  <option>HR</option>
                  <option>Data Scientist</option>
                  <option>Software Engineer</option>
                  <option>Sales</option>
                  <option>Marketing</option>
                  <option>Designer</option>
                  <option>Project Manager</option>
                </Form.Select>
              </FloatingLabel>
            </Col>
          </Row>

          {/* Industry */}
          <FloatingLabel label="Industry" className="dense mb-3">
            <Form.Select name="Industry" required>
              <option value="">Select Industry</option>
              <option>Healthcare</option>
              <option>IT</option>
              <option>Education</option>
              <option>Finance</option>
              <option>Consulting</option>
              <option>Manufacturing</option>
              <option>Retail</option>
            </Form.Select>
          </FloatingLabel>

          <Row>
            {/* Work Location */}
            <Col md>
              <FloatingLabel label="Work Location" className="dense mb-3">
                <Form.Select name="Work_Location" required>
                  <option value="">Select Work Location</option>
                  <option>Hybrid</option>
                  <option>Remote</option>
                  <option>Onsite</option>
                </Form.Select>
              </FloatingLabel>
            </Col>

            {/* Years of Experience */}
            <Col md>
              <FloatingLabel label="Years of Experience" className="dense mb-3">
                <Form.Control
                  name="Years_of_Experience"
                  type="number"
                  placeholder="Years of Experience"
                  min={0}
                  max={65 - 18}
                  step={1}
                  required
                />
              </FloatingLabel>
            </Col>
          </Row>

          {/* Hours Worked Per Week */}
          <FloatingLabel label="Hours Worked Per Week" className="dense mb-3">
            <Form.Control
              name="Hours_Worked_Per_Week"
              type="number"
              placeholder="Hours Worked Per Week"
              min={0}
              step={1}
              required
            />
          </FloatingLabel>

          {/* Number of Virtual Meetings */}
          <FloatingLabel
            label="Number of Virtual Meetings"
            className="dense mb-3"
          >
            <Form.Control
              name="Number_of_Virtual_Meetings"
              type="number"
              placeholder="Number of Virtual Meetings"
              min={0}
              step={1}
              required
            />
          </FloatingLabel>

          <Row>
            {/* Work Life Balance Rating */}
            <Col md>
              <FloatingLabel
                label="Work Life Balance Rating"
                className="dense mb-3"
              >
                <Form.Control
                  name="Work_Life_Balance_Rating"
                  type="number"
                  placeholder="Work Life Balance Rating"
                  min={1}
                  max={5}
                  step={1}
                  required
                />
              </FloatingLabel>
            </Col>

            {/* Stress Level */}
            <Col md>
              <FloatingLabel label="Stress Level" className="dense mb-3">
                <Form.Select name="Stress_Level">
                  <option value="">Select Stress Level</option>
                  <option>Low</option>
                  <option>Medium</option>
                  <option>High</option>
                </Form.Select>
              </FloatingLabel>
            </Col>
          </Row>

          <Row>
            {/* Mental Health Condition */}
            <Col md>
              <FloatingLabel
                label="Mental Health Condition"
                className="dense mb-3"
              >
                <Form.Select name="Mental_Health_Condition" required>
                  <option value="">Select Mental Health Condition</option>
                  <option>Depression</option>
                  <option>Anxiety</option>
                  <option>Burnout</option>
                  <option>None</option>
                </Form.Select>
              </FloatingLabel>
            </Col>

            {/* Access to Mental Health Resources */}
            <Col md>
              <FloatingLabel
                label="Access to Mental Health Resources"
                className="dense mb-3"
              >
                <Form.Select name="Access_to_Mental_Health_Resources" required>
                  <option value="">
                    Select Access to Mental Health Resources
                  </option>
                  <option>No</option>
                  <option>Yes</option>
                </Form.Select>
              </FloatingLabel>
            </Col>
          </Row>

          {/* Productivity Change */}
          <FloatingLabel label="Productivity Change" className="dense mb-3">
            <Form.Select name="Productivity_Change" required>
              <option value="">Select Productivity Change</option>
              <option>Decrease</option>
              <option>No Change</option>
              <option>Increase</option>
            </Form.Select>
          </FloatingLabel>
          <Row>
            {/* Social Isolation Rating */}
            <Col md>
              <FloatingLabel
                label="Social Isolation Rating"
                className="dense mb-3"
              >
                <Form.Control
                  name="Social_Isolation_Rating"
                  type="number"
                  placeholder="Social Isolation Rating"
                  min={1}
                  max={5}
                  step={1}
                  required
                />
              </FloatingLabel>
            </Col>
            <Col md>
              <FloatingLabel
                label="Company Support for Remote Work"
                className="dense mb-3"
              >
                <Form.Control
                  name="Company_Support_for_Remote_Work"
                  type="number"
                  placeholder="Company Support for Remote Work"
                  min={1}
                  max={5}
                  step={1}
                  required
                />
              </FloatingLabel>
            </Col>
          </Row>

          <Row>
            {/* Satisfaction with Remote Work */}
            <Col md>
              <FloatingLabel
                label="Satisfaction with Remote Work"
                className="dense mb-3"
              >
                <Form.Select name="Satisfaction_with_Remote_Work" required>
                  <option value="">Select Satisfaction with Remote Work</option>
                  <option>Unsatisfied</option>
                  <option>Neutral</option>
                  <option>Satisfied</option>
                </Form.Select>
              </FloatingLabel>
            </Col>

            {/* Physical Activity */}
            <Col md>
              <FloatingLabel label="Physical Activity" className="dense mb-3">
                <Form.Select name="Physical_Activity" required>
                  <option value="">Select Physical Activity</option>
                  <option>Weekly</option>
                  <option>Daily</option>
                  <option>None</option>
                </Form.Select>
              </FloatingLabel>
            </Col>
          </Row>

          {/* Sleep Quality */}
          <FloatingLabel label="Sleep Quality" className="dense mb-3">
            <Form.Select name="Sleep_Quality" required>
              <option value="">Select Sleep Quality</option>
              <option>Poor</option>
              <option>Average</option>
              <option>Good</option>
            </Form.Select>
          </FloatingLabel>

          {/* Region */}
          <FloatingLabel label="Region" className="dense mb-3">
            <Form.Select name="Region" required>
              <option value="">Select Region</option>
              <option>Europe</option>
              <option>Asia</option>
              <option>North America</option>
              <option>South America</option>
              <option>Oceania</option>
              <option>Africa</option>
            </Form.Select>
          </FloatingLabel>

          {/* Submit Button */}
          <bd.Button
            // color="white"
            style={{ backgroundColor: "white", color: "black" }}
            size="lg"
            type="submit"
            className="d-block m-auto w-100"
          >
            SUBMIT
          </bd.Button>
        </Form>
        {error && <div style={{ color: "red" }}>{error}</div>}
      </bd.Paper>
    </>
  );
}
