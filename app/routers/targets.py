from typing import Dict, List, Any, Optional
from xml.etree.ElementTree import tostring

from fastapi import APIRouter, Depends, HTTPException, status

from app.gvm_tools.gvm import status_response_code_ok
from app.gvm_tools.targets import GVMTargets
from app.models.target import Target, TargetCreate, TargetUpdate, GetTargetResponse, GetTargetsResponse, \
    CreateTargetResponse
from app.routers.auth import authorization
from app.routers.response import UNAUTHORIZED, INTERNAL_SERVER_ERROR, BAD_REQUEST


class TargetsRouter(APIRouter):
    def __init__(self, gvm_targets: GVMTargets) -> None:
        super().__init__(
            prefix="/v1/targets",
            tags=["targets"],
            dependencies=[Depends(authorization)]
        )
        self._gvm_targets = gvm_targets

        # GET Target
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "/{uuid}",
            self.get_target,
            methods=["GET"],
            response_model=GetTargetResponse,
            responses=http_responses
        )

        # GET Targets
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "",
            self.get_targets,
            methods=["GET"],
            response_model=GetTargetsResponse,
            responses=http_responses
        )

        # POST Create Targets
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        http_responses.update(BAD_REQUEST)
        self.add_api_route(
            "",
            self.create_target,
            methods=["POST"],
            status_code=201,
            response_model=CreateTargetResponse,
            response_description="uuid of the created target",
            responses=http_responses
        )

        # PUT Target
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "/{uuid}",
            self.update_target,
            methods=["PUT"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

        # DELETE Target
        http_responses = {}
        http_responses.update(UNAUTHORIZED)
        http_responses.update(INTERNAL_SERVER_ERROR)
        self.add_api_route(
            "/{uuid}",
            self.delete_target,
            methods=["DELETE"],
            status_code=204,
            response_model=None,
            responses=http_responses,
        )

    async def get_target(self, uuid: str) -> Dict[str, Target]:
        resp = self._gvm_targets.get_target(uuid)
        if not status_response_code_ok(resp, 200):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )
        target = resp.findall("./target")
        if len(target) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="target not found"
            )
        elif len(target) > 1:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="multiple targets with same uuid found"
            )
        return {"target": Target.from_xml(tostring(target[0]))}

    async def get_targets(self, filter_str: Optional[str] = None, trash: Optional[bool] = False) -> Dict[
        str, List[Target]]:
        resp = self._gvm_targets.get_targets(filter_str, trash)
        if not status_response_code_ok(resp, 200):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )
        targets = resp.findall("./target")
        res = []
        for t in targets:
            res.append(Target.from_xml(tostring(t)))
        return {"targets": res}

    async def create_target(self, target: TargetCreate) -> Dict[str, str]:
        if target.port_range is None and target.port_list_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="one of port_list_id or port_range are required"
            )

        resp = self._gvm_targets.create_target(
            target.name,
            asset_hosts_filter=target.asset_hosts_filter,
            hosts=target.hosts,
            comment=target.comment,
            exclude_hosts=target.exclude_hosts,
            ssh_credential_id=target.ssh_credential_id,
            ssh_credential_port=target.ssh_credential_port,
            smb_credential_id=target.smb_credential_id,
            esxi_credential_id=target.esxi_credential_id,
            snmp_credential_id=target.snmp_credential_id,
            alive_test=target.alive_test,
            allow_simultaneous_ips=target.allow_simultaneous_ips,
            reverse_lookup_only=target.reverse_lookup_only,
            reverse_lookup_unify=target.reverse_lookup_unify,
            port_range=target.port_range,
            port_list_id=target.port_list_id
        )
        if not status_response_code_ok(resp, 201):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not created"
            )
        return {"id": resp.get("id")}

    async def update_target(self, uuid: str, target: TargetUpdate) -> Any:
        resp = self._gvm_targets.update_target(
            uuid,
            name=target.name,
            comment=target.comment,
            hosts=target.hosts,
            exclude_hosts=target.exclude_hosts,
            ssh_credential_id=target.ssh_credential_id,
            ssh_credential_port=target.ssh_credential_port,
            smb_credential_id=target.smb_credential_id,
            esxi_credential_id=target.esxi_credential_id,
            snmp_credential_id=target.snmp_credential_id,
            alive_test=target.alive_test,
            allow_simultaneous_ips=target.allow_simultaneous_ips,
            reverse_lookup_only=target.reverse_lookup_only,
            reverse_lookup_unify=target.reverse_lookup_unify,
            port_list_id=target.port_list_id
        )
        if not status_response_code_ok(resp, 200):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )

    async def delete_target(self, uuid: str, ultimate: Optional[bool] = False) -> Any:
        resp = self._gvm_targets.delete_target(uuid, ultimate=ultimate)
        if not status_response_code_ok(resp, 200):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="status code not ok"
            )
