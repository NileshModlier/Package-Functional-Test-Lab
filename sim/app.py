"""Package Sim HTTP application. SIMULATED. Not a vendor product."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from . import learning, quality, workorders
from .defects import list_defects, set_enabled
from .models import SimError, store
from . import DISCLAIMER

BASE = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE / "templates"))
templates.env.globals["disclaimer"] = DISCLAIMER

app = FastAPI(
    title="Package Sim",
    description=DISCLAIMER,
    version="M2",
)
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")


@app.middleware("http")
async def mark_simulated(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Simulated"] = "true"
    return response


@app.exception_handler(SimError)
async def handle_sim_error(_: Request, exc: SimError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "simulated": True},
    )


class EnrollIn(BaseModel):
    learner_id: str
    activity_id: str


class EvaluationIn(BaseModel):
    interaction_id: str


class ScoreIn(BaseModel):
    score: float


class SectionsIn(BaseModel):
    sections: list[dict]


class CommentIn(BaseModel):
    comment: str = ""


class NoteIn(BaseModel):
    note: str = ""


class OrderIn(BaseModel):
    title: str
    requester_id: str
    building: str
    request_class: str
    description: str


class TransitionIn(BaseModel):
    to: str
    actor_id: str | None = None
    reason: str | None = None


class AssignIn(BaseModel):
    technician_id: str


class TimeIn(BaseModel):
    technician_id: str
    hours: float = Field(gt=0)


class MaterialIn(BaseModel):
    item_id: str
    quantity: float


class DefectIn(BaseModel):
    enabled: bool


def _page(request: Request, name: str, **extra):
    return templates.TemplateResponse(
        request,
        name,
        {
            "error": request.query_params.get("error"),
            "disclaimer": DISCLAIMER,
            **extra,
        },
    )


def _back(path: str, exc: SimError | None = None) -> RedirectResponse:
    target = path if exc is None else f"{path}?error={quote(exc.message)}"
    return RedirectResponse(target, status_code=303)


@app.get("/health")
def health():
    return {"status": "ok", "simulated": True, "service": "package-sim"}


@app.post("/test/reset")
def test_reset():
    store.reset()
    return {"status": "reset", "simulated": True}


@app.get("/")
def home(request: Request):
    return _page(
        request,
        "index.html",
        learners=len(store.data["learners"]),
        evaluations=len(store.data["evaluations"]),
        work_orders=len(store.data["work_orders"]),
    )


@app.get("/learning")
def learning_page(request: Request):
    return _page(
        request,
        "learning.html",
        activities=learning.list_activities(),
        learners=learning.list_learners(),
        enrollments=learning.list_enrollments(),
        certificates=learning.list_certificates(),
    )


@app.get("/quality")
def quality_page(request: Request):
    return _page(
        request,
        "quality.html",
        interactions=quality.list_interactions(),
        evaluations=quality.list_evaluations(),
    )


@app.get("/workorders")
def work_page(request: Request):
    return _page(
        request,
        "workorders.html",
        orders=workorders.list_orders(),
        technicians=workorders.list_technicians(),
        states=["Draft", "WAPPR", "APPR", "INPRG", "WMATL", "COMP", "CLOSE"],
    )


@app.get("/defects")
def defects_page(request: Request):
    return _page(request, "defects.html", defects=list_defects())


@app.get("/api/learning/activities")
def api_activities():
    return learning.list_activities()


@app.get("/api/learning/learners")
def api_learners():
    return learning.list_learners()


@app.get("/api/learning/enrollments")
def api_enrollments():
    return learning.list_enrollments()


@app.get("/api/learning/certificates")
def api_certificates():
    return learning.list_certificates()


@app.post("/api/learning/enrollments")
def api_enroll(body: EnrollIn):
    return learning.enroll(body.learner_id, body.activity_id)


@app.post("/api/learning/enrollments/{enrollment_id}/start")
def api_start(enrollment_id: str):
    return learning.start(enrollment_id)


@app.post("/api/learning/enrollments/{enrollment_id}/assessment")
def api_assess(enrollment_id: str, body: ScoreIn):
    return learning.assess(enrollment_id, body.score)


@app.post("/api/learning/enrollments/{enrollment_id}/reset")
def api_reset_attempt(enrollment_id: str):
    return learning.reset_attempt(enrollment_id)


@app.post("/api/learning/enrollments/{enrollment_id}/complete")
def api_complete_learning(enrollment_id: str):
    return learning.complete(enrollment_id)


@app.get("/api/quality/interactions")
def api_interactions():
    return quality.list_interactions()


@app.get("/api/quality/evaluations")
def api_evaluations():
    return quality.list_evaluations()


@app.post("/api/quality/evaluations")
def api_create_evaluation(body: EvaluationIn):
    return quality.create_evaluation(body.interaction_id)


@app.post("/api/quality/evaluations/{evaluation_id}/submit")
def api_submit(evaluation_id: str, body: SectionsIn):
    return quality.submit(evaluation_id, body.sections)


@app.post("/api/quality/evaluations/{evaluation_id}/acknowledge")
def api_ack(evaluation_id: str):
    return quality.acknowledge(evaluation_id)


@app.post("/api/quality/evaluations/{evaluation_id}/dispute")
def api_dispute(evaluation_id: str, body: CommentIn):
    return quality.dispute(evaluation_id, body.comment)


@app.post("/api/quality/evaluations/{evaluation_id}/resolve")
def api_resolve(evaluation_id: str):
    return quality.resolve(evaluation_id)


@app.post("/api/quality/evaluations/{evaluation_id}/coach")
def api_coach(evaluation_id: str, body: NoteIn):
    return quality.coach(evaluation_id, body.note)


@app.post("/api/quality/evaluations/{evaluation_id}/complete")
def api_complete_quality(evaluation_id: str):
    return quality.complete(evaluation_id)


@app.get("/api/work/orders")
def api_orders():
    return workorders.list_orders()


@app.get("/api/work/technicians")
def api_technicians():
    return workorders.list_technicians()


@app.post("/api/work/orders")
def api_create_order(body: OrderIn):
    return workorders.create_order(body.model_dump())


@app.post("/api/work/orders/{order_id}/transition")
def api_transition(order_id: str, body: TransitionIn):
    return workorders.transition(order_id, body.to, body.actor_id, body.reason)


@app.post("/api/work/orders/{order_id}/assign")
def api_assign(order_id: str, body: AssignIn):
    return workorders.assign(order_id, body.technician_id)


@app.post("/api/work/orders/{order_id}/time")
def api_time(order_id: str, body: TimeIn):
    return workorders.add_time(order_id, body.technician_id, body.hours)


@app.post("/api/work/orders/{order_id}/materials")
def api_material(order_id: str, body: MaterialIn):
    return workorders.add_material(order_id, body.item_id, body.quantity)


@app.get("/api/defects")
def api_defects():
    return list_defects()


@app.post("/api/defects/{defect_id}")
def api_set_defect(defect_id: str, body: DefectIn):
    return set_enabled(defect_id, body.enabled)


@app.post("/ui/learning/enroll")
def ui_enroll(learner_id: str = Form(...), activity_id: str = Form(...)):
    try:
        learning.enroll(learner_id, activity_id)
    except SimError as exc:
        return _back("/learning", exc)
    return _back("/learning")


@app.post("/ui/learning/enrollments/{enrollment_id}/start")
def ui_start(enrollment_id: str):
    try:
        learning.start(enrollment_id)
    except SimError as exc:
        return _back("/learning", exc)
    return _back("/learning")


@app.post("/ui/learning/enrollments/{enrollment_id}/assessment")
def ui_assess(enrollment_id: str, score: float = Form(...)):
    try:
        learning.assess(enrollment_id, score)
    except SimError as exc:
        return _back("/learning", exc)
    return _back("/learning")


@app.post("/ui/learning/enrollments/{enrollment_id}/complete")
def ui_complete_learning(enrollment_id: str):
    try:
        learning.complete(enrollment_id)
    except SimError as exc:
        return _back("/learning", exc)
    return _back("/learning")


@app.post("/ui/quality/evaluations/{evaluation_id}/submit")
def ui_submit(
    evaluation_id: str,
    earned_a: float = Form(...),
    earned_b: float = Form(...),
    earned_c: float = Form(...),
):
    sections = [
        {"id": "A", "earned": earned_a, "possible": 2},
        {"id": "B", "earned": earned_b, "possible": 1},
        {"id": "C", "earned": earned_c, "possible": 1},
    ]
    try:
        quality.submit(evaluation_id, sections)
    except SimError as exc:
        return _back("/quality", exc)
    return _back("/quality")


@app.post("/ui/quality/evaluations/{evaluation_id}/acknowledge")
def ui_ack(evaluation_id: str):
    try:
        quality.acknowledge(evaluation_id)
    except SimError as exc:
        return _back("/quality", exc)
    return _back("/quality")


@app.post("/ui/quality/evaluations/{evaluation_id}/resolve")
def ui_resolve(evaluation_id: str):
    try:
        quality.resolve(evaluation_id)
    except SimError as exc:
        return _back("/quality", exc)
    return _back("/quality")


@app.post("/ui/quality/evaluations/{evaluation_id}/dispute")
def ui_dispute(evaluation_id: str, comment: str = Form(...)):
    try:
        quality.dispute(evaluation_id, comment)
    except SimError as exc:
        return _back("/quality", exc)
    return _back("/quality")


@app.post("/ui/quality/evaluations/{evaluation_id}/coach")
def ui_coach(evaluation_id: str, note: str = Form(...)):
    try:
        quality.coach(evaluation_id, note)
    except SimError as exc:
        return _back("/quality", exc)
    return _back("/quality")


@app.post("/ui/quality/evaluations/{evaluation_id}/complete")
def ui_complete_quality(evaluation_id: str):
    try:
        quality.complete(evaluation_id)
    except SimError as exc:
        return _back("/quality", exc)
    return _back("/quality")


@app.post("/ui/work/orders")
def ui_create_order(
    title: str = Form(...),
    requester_id: str = Form(...),
    building: str = Form(...),
    request_class: str = Form(...),
    description: str = Form(...),
):
    try:
        workorders.create_order(
            {
                "title": title,
                "requester_id": requester_id,
                "building": building,
                "request_class": request_class,
                "description": description,
            }
        )
    except SimError as exc:
        return _back("/workorders", exc)
    return _back("/workorders")


@app.post("/ui/work/orders/{order_id}/transition")
def ui_transition(
    order_id: str,
    to: str = Form(...),
    actor_id: str = Form(""),
    reason: str = Form(""),
):
    try:
        workorders.transition(order_id, to, actor_id or None, reason or None)
    except SimError as exc:
        return _back("/workorders", exc)
    return _back("/workorders")


@app.post("/ui/work/orders/{order_id}/assign")
def ui_assign(order_id: str, technician_id: str = Form(...)):
    try:
        workorders.assign(order_id, technician_id)
    except SimError as exc:
        return _back("/workorders", exc)
    return _back("/workorders")


@app.post("/ui/defects/{defect_id}")
def ui_defect(defect_id: str, enabled: str = Form(...)):
    try:
        set_enabled(defect_id, enabled == "true")
    except SimError as exc:
        return _back("/defects", exc)
    return _back("/defects")
